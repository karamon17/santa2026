from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class QuizQuestion:
    prompt: str
    options: Dict[str, str]
    correct: str


@dataclass
class UserState:
    score: int = 0
    current_index: int = 0
    incorrect_queue: List[int] = field(default_factory=list)
    active_question: Optional[int] = None
    sent_safety: bool = False
    sent_parking: bool = False
    sent_inspiration: bool = False
    finished: bool = False
    postgame: bool = False
