from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.case import router as case_router
from app.api.stream import router as stream_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Women's Inheritance Rights Recovery Platform"
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
