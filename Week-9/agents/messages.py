from dataclasses import dataclass
from typing import List

@dataclass
class UserTask:
    task: str

@dataclass
class WorkerTask:
    task: str
    previous_results: List[str]

@dataclass
class WorkerTaskResult:
    result: str

@dataclass
class ReflectionTask:
    task: str
    worker_outputs: List[str]

@dataclass
class ReflectedResult:
    result: str

@dataclass
class ValidationTask:
    task: str
    answer: str

@dataclass
class ValidationResult:
    is_valid: bool
    feedback: str
    answer: str

@dataclass
class FinalResult:
    result: str

@dataclass
class ExecutionNode:
    name: str
    output: str
    children: List["ExecutionNode"]
