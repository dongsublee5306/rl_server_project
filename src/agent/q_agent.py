import pickle
import os
from collections import defaultdict
import random
from src.contracts.action import Action

Q_TABLE_PATH = "q_table.pkl"

class QAgent:
    def __init__(self, lr=0.1, gamma=0.9, epsilon=0.1):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = list(Action)

        if os.path.exists(Q_TABLE_PATH):
            with open(Q_TABLE_PATH, "rb") as f:
                self.q = pickle.load(f)
            print("✅ Q-table loaded")
        else:
            self.q = defaultdict(float)

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        qs = [self.q[(state, a)] for a in self.actions]
        return self.actions[qs.index(max(qs))]

    def update(self, state, action, reward, next_state):
        max_next = max(self.q[(next_state, a)] for a in self.actions)
        self.q[(state, action)] += self.lr * (
            reward + self.gamma * max_next - self.q[(state, action)]
        )

    def save(self):
        with open(Q_TABLE_PATH, "wb") as f:
            pickle.dump(self.q, f)
        print("💾 Q-table saved")
