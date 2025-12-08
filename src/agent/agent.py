# src/agent/agent.py
from src.contracts.element import Element
from src.environment.env import Environment

class Agent:
    def __init__(self, env: Environment):
        self.env = env
        self.memory = []

    def step(self):
        state = self.env.get_state()
        action = self.select_action(state)

        next_state, reward, done = self.env.step(action)

        element = Element(
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=done
        )

        self.memory.append(element)
        self.learn(element)

        return element

    def select_action(self, state):
        # 임시 (나중에 Q-table / NN)
        return Action.LEFT

    def learn(self, element: Element):
        pass
