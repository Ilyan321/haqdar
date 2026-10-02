from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from app.services.session_store import session_store
from app.services.event_broadcaster import event_broadcaster

router = APIRouter(prefix="/case", tags=["Streaming Telemetry"])

@router.get("/stream/{session_id}")
async def stream_agent_telemetry(session_id: str):
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    return EventSourceResponse(
        event_broadcaster.stream(session_id),
        media_type="text/event-stream"
    )
