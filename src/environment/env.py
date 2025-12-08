print("🔥 env.py LOADED 🔥")

import random
from src.contracts.state import State
from src.contracts.action import Action

class Environment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.car_lane = 1              # ✅ 가운데 시작 (0,1,2)
        self.obstacles = []            # ✅ 매 episode 초기화
        self.timestep = 0
        return self.get_state()

    def spawn_obstacle(self):
        # ✅ 일정 확률로 새 장애물 생성
        if random.random() < 0.3:      # ← 난이도 조절 포인트
            lane = random.randint(0, 2)
            self.obstacles.append((lane, 5))

    def get_state(self):
        return State(self.car_lane, tuple(self.obstacles))

    def step(self, action: Action):
        done = False
        reward = 1
        self.timestep += 1

        # ✅ 차량 이동 (차선 3개 고정)
        if action == Action.LEFT and self.car_lane > 0:
            self.car_lane -= 1
        elif action == Action.RIGHT and self.car_lane < 2:
            self.car_lane += 1

        # ✅ 장애물 이동
        new_obstacles = []
        for lane, y in self.obstacles:
            y -= 1
            if y >= 0:
                new_obstacles.append((lane, y))
        self.obstacles = new_obstacles

        # ✅ 새 장애물 생성
        self.spawn_obstacle()

        # ✅ 충돌 체크
        for lane, y in self.obstacles:
            if lane == self.car_lane and y == 0:
                reward = -10
                done = True
                break

        return self.get_state(), reward, done
