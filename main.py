import json
import os
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- 管理员密码 (你可以修改这里) ---
ADMIN_PASSWORD = "8888"

# --- 1. 数据存储核心逻辑 ---
class PollManager:
    def __init__(self):
        self.current_poll: Dict[str, Any] = None
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_update(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_update(self, websocket: WebSocket):
        if not self.current_poll:
            await websocket.send_text(json.dumps({"type": "POLL_DELETED"}))
        else:
            await websocket.send_text(json.dumps({
                "type": "UPDATE_STATE",
                "data": self.current_poll
            }))

    async def broadcast(self):
        if not self.current_poll:
            message = json.dumps({"type": "POLL_DELETED"})
        else:
            message = json.dumps({
                "type": "UPDATE_STATE",
                "data": self.current_poll
            })
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

    async def create_poll(self, data: dict):
        self.current_poll = {
            "question": data['question'],
            "options": [{"id": i, "text": t, "count": 0} for i, t in enumerate(data['options'])],
            "groups": data['groups'],
            "groupVotes": {g: 0 for g in data['groups']},
            "totalVotes": 0,
            "status": "active"
        }
        await self.broadcast()

    async def cast_vote(self, option_index: int, group: str):
        if not self.current_poll:
            return

        # 检查 5 票限制
        current_group_votes = self.current_poll["groupVotes"].get(group, 0)
        if current_group_votes >= 5:
            return 

        self.current_poll["options"][option_index]["count"] += 1
        self.current_poll["totalVotes"] += 1
        self.current_poll["groupVotes"][group] += 1
        
        await self.broadcast()

    async def delete_poll(self):
        self.current_poll = None
        await self.broadcast()

manager = PollManager()

# --- 2. WebSocket 路由 (增加了密码检查) ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            action = payload.get("action")
            
            # --- 权限检查逻辑 ---
            if action in ["create_poll", "delete_poll"]:
                if payload.get("password") != ADMIN_PASSWORD:
                    await websocket.send_text(json.dumps({
                        "type": "ERROR", 
                        "message": "密码错误，无权操作"
                    }))
                    continue
            # ------------------

            if action == "create_poll":
                await manager.create_poll(payload["data"])
            elif action == "vote":
                await manager.cast_vote(payload["optionIndex"], payload["group"])
            elif action == "delete_poll":
                await manager.delete_poll()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

@app.get("/")
async def get_index():
    # 默认页面 (学生端/控制端)
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/screen")
async def get_screen():
    # 新增：大屏专用页面 (只显示结果)
    # 如果文件不存在，请确保创建了 screen.html
    if os.path.exists("screen.html"):
        with open("screen.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("请先创建 screen.html 文件", status_code=404)
