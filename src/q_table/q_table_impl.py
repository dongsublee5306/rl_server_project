from typing import Dict, Tuple
from src.contracts import QTable, State, Action, Element


class QTableImpl(QTable):
    def __init__(self, alpha=0.1, gamma=0.9):
        self.alpha = alpha
        self.gamma = gamma
        self.table: Dict[Tuple[State, Action], float] = {}

    def get_q_value(self, state: State, action: Action) -> float:
        return self.table.get((state, action), 0.0)

    def get_max_q_value(self, state: State) -> float:
        return max(
            self.get_q_value(state, action)
            for action in Action
        )

    def update(self, element: Element) -> None:
        s = element.state
        a = element.action
        r = element.reward.value
        s_next = element.next_state

        old_q = self.get_q_value(s, a)
        new_q = old_q + self.alpha * (
            r + self.gamma * self.get_max_q_value(s_next) - old_q
        )

        self.table[(s, a)] = new_q
