import asyncio
import json
from typing import Dict, AsyncGenerator, Any
from pydantic import BaseModel

class AgentTelemetryEvent(BaseModel):
    case_id: str
    agent_id: str
    status: str  # 'idle' | 'started' | 'thinking' | 'tool_call' | 'completed' | 'reflecting' | 'error'
    message: str
    tool: str = ""
    data: Dict[str, Any] = {}
    timestamp: float = 0.0

class SSEEventBroadcaster:
    """
    Manages asynchronous SSE event queues per session, allowing 
    CrewAI agent status updates to stream directly to Next.js clients in real-time.
    """
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}

    def get_or_create_queue(self, session_id: str) -> asyncio.Queue:
        if session_id not in self._queues:
            self._queues[session_id] = asyncio.Queue()
        return self._queues[session_id]

    async def broadcast(self, session_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        queue = self.get_or_create_queue(session_id)
        formatted_message = {
            "event": event_type,
            "data": payload
        }
        await queue.put(formatted_message)

    async def stream(self, session_id: str) -> AsyncGenerator[str, None]:
        queue = self.get_or_create_queue(session_id)
        try:
            while True:
                message = await queue.get()
                event_name = message.get("event", "message")
                data_json = json.dumps(message.get("data", {}))
                yield f"event: {event_name}\ndata: {data_json}\n\n"
                queue.task_done()
        except asyncio.CancelledError:
            # Client disconnected
            pass

    def remove_session(self, session_id: str) -> None:
        self._queues.pop(session_id, None)

event_broadcaster = SSEEventBroadcaster()
