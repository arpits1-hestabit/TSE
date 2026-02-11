import json
import os
from semantic_memory import SemanticMemory


class OrchestratorAgent:
    """
    DAG-based multi-agent orchestrator responsible for:
    - Executing agents based on dependency graph
    - Enforcing per-agent confidence contracts
    - Retrying validation-driven optimizations
    """

    AGENT_GRAPH = {
        "Researcher": [],
        "Analyst": [],
        "Coder": ["Researcher"],
        "Critic": ["Coder"],
        "Optimizer": ["Coder", "Critic"],
        "Validator": ["Optimizer"],
    }

    MAX_VALIDATION_RETRIES = 2
    MAX_CONFIDENCE_RETRIES = 2

    LOW_CONFIDENCE_THRESHOLD = 0.6
    CONFIDENCE_FALLBACK = 0.3

    def __init__(self, agents, logger, output_dir="outputs"):
        """
        Initialize orchestrator with agents, logger, and persistent memory.
        """
        self.agents = agents
        self.logger = logger
        self.memory = SemanticMemory()

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # Helper functions for memory, dependency checking, and confidence parsing

    def build_memory_context(self, query: str) -> str:
        """
        Retrieve semantically similar past outputs to enrich agent prompts.
        """
        recalled = self.memory.search(query, k=2)
        if not recalled:
            return ""

        context = "\n\nRelevant Past Memory:\n"
        for mem in recalled:
            context += f"- {mem[:200]}...\n"
        return context

    def dependencies_satisfied(self, agent_name, results):
        """
        Check whether all dependency agents have completed execution.
        """
        return all(dep in results for dep in self.AGENT_GRAPH.get(agent_name, []))

    def extract_confidence(self, output: str):
        """
        Parse CONFIDENCE score from agent output.
        """
        if "CONFIDENCE:" not in output:
            return None
        try:
            score = float(output.split("CONFIDENCE:")[-1].strip())
            if 0.0 <= score <= 1.0:
                return score
        except Exception:
            pass
        return None

    def strip_confidence(self, output: str) -> str:
        """
        Remove confidence line from agent output before downstream usage.
        """
        return output.split("CONFIDENCE:")[0].strip()

    async def run_agent_with_confidence(self, agent_name, prompt):
        """
        Execute an agent while enforcing confidence contract and retries.
        """
        raw_output = None
        conf_score = None

        for _ in range(self.MAX_CONFIDENCE_RETRIES):
            raw_output = await self.agents[agent_name].run(prompt)
            conf_score = self.extract_confidence(raw_output)

            if conf_score is not None:
                break

            self.logger.warning(
                f"{agent_name} did not return valid CONFIDENCE. Retrying..."
            )

        if conf_score is None:
            conf_score = self.CONFIDENCE_FALLBACK
            self.logger.error(
                f"{agent_name} violated confidence contract. "
                f"Assigned fallback CONFIDENCE={conf_score}"
            )

        clean_output = self.strip_confidence(raw_output)

        self.logger.info(f"[CONFIDENCE] {agent_name}: {conf_score:.2f}")

        if conf_score < self.LOW_CONFIDENCE_THRESHOLD:
            self.logger.warning(
                f"[LOW CONFIDENCE] {agent_name}: {conf_score:.2f}"
            )

        return clean_output, conf_score

    # Main execution loop

    async def run(self, user_question: str, plan_json: str):
        """
        Execute the DAG-based multi-agent workflow end-to-end.
        """
        plan = json.loads(plan_json)
        results = {}
        confidence = {}

        self.logger.info("Executing DAG-based multi-agent workflow...")

        pending_agents = {
            task["agent"]: task["task"]
            for task in plan["tasks"]
            if task["agent"] != "Reporter"
        }

        while pending_agents:
            progressed = False

            for agent_name in list(pending_agents.keys()):
                if agent_name not in self.agents:
                    self.logger.warning(f"Agent '{agent_name}' not found. Skipping.")
                    pending_agents.pop(agent_name)
                    continue

                if not self.dependencies_satisfied(agent_name, results):
                    continue

                base_task = pending_agents.pop(agent_name)
                progressed = True

                self.logger.info(f"Executing {agent_name}...")

                memory_context = self.build_memory_context(base_task)

                dependency_context = ""
                for dep in self.AGENT_GRAPH.get(agent_name, []):
                    dependency_context += f"\n\n{dep} OUTPUT:\n{results[dep][:1200]}"

                final_prompt = f"""
                TASK:
                {base_task}

                {memory_context}

                {dependency_context}

                You MUST always include a final line:
                CONFIDENCE: <number between 0 and 1>

                Use this scale:
                - 0.9-1.0: Deterministic, well-known, no assumptions
                - 0.7-0.9: Mostly confident, minor assumptions
                - 0.5-0.7: Reasonable but incomplete or uncertain
                - 0.3-0.5: Speculative, multiple assumptions
                - <0.3: Guessing or low reliability
                """

                output, conf = await self.run_agent_with_confidence(
                    agent_name, final_prompt
                )

                results[agent_name] = output
                confidence[agent_name] = conf
                self.memory.add(base_task, output)

                # Validation retries if Validator fails
                if agent_name == "Validator":
                    retries = 0

                    while retries < self.MAX_VALIDATION_RETRIES:
                        if "VALIDATION_STATUS: FAIL" not in output:
                            break

                        self.logger.warning(
                            f"Validation failed. Retrying optimization ({retries + 1})..."
                        )

                        optimizer = self.agents.get("Optimizer")
                        if not optimizer:
                            break

                        retry_prompt = f"""
                        Fix ONLY the issues reported by the validator.
                        Do NOT restate the entire solution.
                        
                        Validator Feedback:
                        {output[:800]}
                        """

                        optimized, opt_conf = await self.run_agent_with_confidence(
                            "Optimizer", retry_prompt
                        )

                        results["Optimizer"] = optimized
                        confidence["Optimizer"] = opt_conf

                        output, val_conf = await self.run_agent_with_confidence(
                            "Validator", optimized
                        )

                        results["Validator"] = output
                        confidence["Validator"] = val_conf

                        retries += 1

            if not progressed:
                self.logger.error("DAG execution stalled due to unmet dependencies.")
                break

        self.logger.info("Final agent confidence summary:")
        for agent, score in confidence.items():
            self.logger.info(f"  - {agent}: {score:.2f}")

        # Report generation with Reporter agent
        if "Reporter" in self.agents:
            self.logger.info("Executing Reporter (Final Compilation)...")

            reporter_output = await self.agents["Reporter"].run(
                user_question,
                {
                    "outputs": results,
                    "confidence": confidence,
                },
            )

            results["Reporter"] = reporter_output

            filename = self.agents["Reporter"].sanitize_filename(user_question)
            path = os.path.join(self.output_dir, filename + ".md")
            self.logger.info(f"Reporter output saved -> {path}")

        return {
            "outputs": results,
            "confidence": confidence,
        }
