import asyncio
import logging
import os
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.case import router as case_router
from app.api.stream import router as stream_router

logger = logging.getLogger(__name__)

async def keep_alive_background_worker():
    """Periodically ping external health endpoint to prevent free tier spin-down."""
    await asyncio.sleep(60)  # Wait 1 minute after server boot before starting loop
    base_url = os.environ.get("RENDER_EXTERNAL_URL", "https://haqdar-backend-dvwu.onrender.com")
    target_url = f"{base_url.rstrip('/')}/health"
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        while True:
            try:
                res = await client.get(target_url)
                logger.info(f"Keep-alive heartbeat pinged {target_url} -> Status: {res.status_code}")
            except Exception as e:
                logger.warning(f"Keep-alive ping note: {e}")
            await asyncio.sleep(600)  # Ping every 10 minutes (Render sleep threshold is 15 minutes)

@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_task = asyncio.create_task(keep_alive_background_worker())
    yield
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Women's Inheritance Rights Recovery Platform",
    lifespan=lifespan
)

# CORS configuration for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development / Next.js local & prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(case_router, prefix=settings.API_PREFIX)
app.include_router(stream_router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "health": "/health",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "primary_model": settings.PRIMARY_MODEL,
        "groq_keys_available": len(settings.groq_key_pool)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
