from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contracts.Element import Element
    from src.contracts.state import State
    from src.contracts.Action import Action

class QTable(ABC):

    @abstractmethod
    def update(self, element: 'Element') -> None:
        pass

    @abstractmethod
    def get_q_value(self, state: 'State', action: 'Action') -> float:
        pass

    @abstractmethod
    def get_max_q_value(self, state: 'State') -> float:
        pass
