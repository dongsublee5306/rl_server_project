from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.environment.env import Environment
from src.contracts.action import Action
from src.agent.q_agent import QAgent

app = FastAPI()

env = Environment()
agent = QAgent()

# ✅ 학습 통계
total_collisions = 0
episode_steps = 0
episode_history = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global total_collisions, episode_steps

    await ws.accept()

    try:
        state = env.reset()
        episode_steps = 0

        # ✅ 초기 상태 전송
        await ws.send_json({
            "type": "init",
            "state": {
                "car_lane": state.car_lane,
                "obstacles": state.obstacles
            }
        })

        while True:
            # ✅ 서버가 스스로 행동 선택
            action = agent.select_action(state)

            # ✅ 환경 진행
            next_state, reward, done = env.step(action)

            # ✅ 학습
            agent.update(state, action, reward, next_state)

            episode_steps += 1
            state = next_state

            # ✅ step 결과 전송
            await ws.send_json({
                "type": "step",
                "action": action.value,
                "reward": reward,
                "state": {
                    "car_lane": state.car_lane,
                    "obstacles": state.obstacles
                },
                "step": episode_steps,
                "total_collisions": total_collisions
            })

            # ✅ 충돌 → 에피소드 종료
            if done:
                total_collisions += 1
                episode_history.append(episode_steps)

                avg_survival = sum(episode_history) / len(episode_history)

                await ws.send_json({
                    "type": "episode_end",
                    "episode_survival": episode_steps,
                    "average_survival": avg_survival,
                    "total_collisions": total_collisions
                })

                # ✅ 환경 리셋 (다음 학습 시작)
                state = env.reset()
                episode_steps = 0

    except WebSocketDisconnect:
        print("client disconnected")
