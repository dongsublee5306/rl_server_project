from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class State:
    car_lane: int
    obstacles: Tuple[Tuple[int, int], ...] = ()

    def __hash__(self):
        return hash((self.car_lane, self.obstacles))
