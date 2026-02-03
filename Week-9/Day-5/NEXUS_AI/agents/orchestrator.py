import json
import os
from semantic_memory import SemanticMemory


class OrchestratorAgent:
    """
    Central coordinator responsible for executing a planner-generated task plan
    using multiple specialized agents, while leveraging semantic memory for
    contextual recall across runs.

    Responsibilities:
    - Executes agent tasks sequentially based on a JSON execution plan
    - Retrieves relevant past context using FAISS-backed semantic memory
    - Injects recalled memory into agent prompts when available
    - Stores new task-response pairs back into memory
    - Delegates final result compilation to the Reporter agent
    - Logs execution progress and output locations

    This class acts as the backbone of the multi-agent execution pipeline.
    """

    def __init__(self, agents, logger, output_dir="outputs"):
        """
        Initializes the OrchestratorAgent.

        :param agents: Dictionary mapping agent names to agent instances
        :param logger: Application logger for structured logging
        :param output_dir: Directory where final reports will be saved
        """
        self.agents = agents
        self.logger = logger

        # Initialize FAISS-based semantic memory
        self.memory = SemanticMemory()

        # Ensure output directory exists
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_memory_context(self, query: str) -> str:
        """
        Builds a contextual memory block for a given query using semantic search.
        If relevant past memories are found, a short summarized context is
        constructed and injected into the agent prompt. If no memory is found,
        an empty string is returned.
        """
        recalled = self.memory.search(query, k=2)

        if not recalled:
            return ""

        context = "\n\nRelevant Past Memory:\n"
        for mem in recalled:
            # Truncate memory to avoid excessively long prompts
            context += f"- {mem[:200]}...\n"

        return context

    async def run(self, user_question: str, plan_json: str):
        """
        Executes a full multi-agent workflow based on a planner-generated plan.

        Workflow:
        1. Parse the JSON execution plan
        2. Execute each agent task (except Reporter)
        3. Inject relevant semantic memory into prompts
        4. Store agent outputs in memory
        5. Run the Reporter agent for final compilation
        """
        plan = json.loads(plan_json)
        results = {}

        self.logger.info("Executing tasks with Semantic Memory...")

        # Execute all agents except Reporter
        for task_item in plan["tasks"]:
            agent_name = task_item["agent"]
            task = task_item["task"]

            # Reporter is executed at the end
            if agent_name == "Reporter":
                continue

            # Skip unknown agents gracefully
            if agent_name not in self.agents:
                self.logger.warning(f"Agent '{agent_name}' not found. Skipping.")
                continue

            self.logger.info(f"Executing {agent_name} task...")

            # Retrieve relevant semantic memory
            memory_context = self.build_memory_context(task)

            # Construct final prompt with optional memory context
            final_prompt = f"""
            TASK:
            {task}

            {memory_context}
            """

            agent = self.agents[agent_name]
            output = await agent.run(final_prompt)

            # Persist task-output pair into semantic memory
            self.memory.add(task, output)

            # Store output for downstream agents
            results[agent_name] = output

        # Execute Reporter agent last for final aggregation
        if "Reporter" in self.agents:
            self.logger.info("Executing Reporter (Final Compilation)...")
            reporter_agent = self.agents["Reporter"]

            reporter_output = await reporter_agent.run(user_question, results)
            results["Reporter"] = reporter_output

            # Log the saved report file path
            sanitized_name = reporter_agent.sanitize_filename(user_question)
            report_path = os.path.join(self.output_dir, sanitized_name + ".md")
            self.logger.info(f"Reporter output saved -> {report_path}")

        else:
            self.logger.warning("Reporter agent not found. Nothing saved.")

        return results
