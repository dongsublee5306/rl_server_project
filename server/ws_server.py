from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.environment.env import Environment
from src.agent.q_agent import QAgent
from src.contracts.action import Action
import json

app = FastAPI()
agent = QAgent()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # ✅ 1단계: 설정 수신
        config_msg = await ws.receive_json()

        config = {
            "lane": config_msg["lane"],
            "obs": config_msg["obs"],
            "frequency": config_msg["frequency"]
        }
        learn = config_msg["learn"]

        env = Environment(config)
        state = env.reset()
        step_count = 0
        collision_count = 0
        history = []

        await ws.send_json({
            "type": "init",
            "state": {
                "car_lane": state.car_lane,
                "obstacles": state.obstacles
            }
        })

        while True:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)

            if learn:
                agent.update(state, action, reward, next_state)

            state = next_state
            step_count += 1

            await ws.send_json({
                "type": "step",
                "action": action.value,
                "reward": reward,
                "state": {
                    "car_lane": state.car_lane,
                    "obstacles": state.obstacles
                },
                "step": step_count,
                "collisions": collision_count
            })

            if done:
                collision_count += 1
                history.append(step_count)

                await ws.send_json({
                    "type": "episode_end",
                    "survival": step_count,
                    "avg_survival": sum(history) / len(history)
                })

                state = env.reset()
                step_count = 0

    except WebSocketDisconnect:
        print("client disconnected")
