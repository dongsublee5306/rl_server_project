# src/contracts/element.py
from dataclasses import dataclass
from src.contracts.state import State
from src.contracts.action import Action

@dataclass
class Element:
    state: State
    action: Action
    reward: float
    next_state: State
    done: bool
