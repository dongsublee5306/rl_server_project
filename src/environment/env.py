from src.contracts.state import State
from src.contracts.action import Action
import random

class Environment:
    def __init__(self, config):
        self.lanes = config["lane"]
        self.max_obs = config["obs"]
        self.frequency = config["frequency"]
        self.step_count = 0
        self.reset()

    def reset(self):
        self.car_lane = self.lanes // 2
        self.obstacles = []
        self.step_count = 0
        return self.get_state()

    def get_state(self):
        return State(self.car_lane, tuple(self.obstacles))

    def spawn_obstacle(self):
        if len(self.obstacles) >= self.max_obs:
            return
        lane = random.randint(0, self.lanes - 1)
        self.obstacles.append((lane, 5))

    def step(self, action: Action):
        self.step_count += 1
        done = False
        reward = 1

        # ✅ 차선 이동 (동적)
        if action == Action.LEFT and self.car_lane > 0:
            self.car_lane -= 1
        elif action == Action.RIGHT and self.car_lane < self.lanes - 1:
            self.car_lane += 1

        # ✅ 장애물 이동
        new_obs = []
        for lane, y in self.obstacles:
            y -= 1
            if y >= 0:
                new_obs.append((lane, y))
        self.obstacles = new_obs

        # ✅ 주기적 장애물 생성
        if self.step_count % self.frequency == 0:
            self.spawn_obstacle()

        # ✅ 충돌 체크
        for lane, y in self.obstacles:
            if lane == self.car_lane and y == 0:
                reward = -10
                done = True

        return self.get_state(), reward, done
