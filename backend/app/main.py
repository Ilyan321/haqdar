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

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def root():
    keys_count = len(settings.groq_key_pool)
    primary_model = settings.PRIMARY_MODEL
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HaqDar API — Core Engine Status</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    code, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="bg-slate-950 text-slate-200 min-h-screen flex flex-col justify-between antialiased selection:bg-teal-500 selection:text-white">
  <!-- Glow Accent -->
  <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-teal-600/15 blur-[120px] pointer-events-none rounded-full"></div>

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-900/40 backdrop-blur px-6 py-4">
    <div class="max-w-4xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-teal-500 to-teal-800 text-white flex items-center justify-center font-bold text-base shadow-lg shadow-teal-900/30">
          حق
        </div>
        <div>
          <span class="font-extrabold text-white tracking-tight">HaqDar (حقدار)</span>
          <span class="text-[10px] text-teal-400 font-mono ml-1.5 px-1.5 py-0.5 bg-teal-950 border border-teal-800/60 rounded">API Core v{settings.VERSION}</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="relative flex h-2.5 w-2.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
        </span>
        <span class="text-xs text-emerald-400 font-medium">Server Active</span>
      </div>
    </div>
  </header>

  <!-- Main Status Card -->
  <main class="flex-1 flex items-center justify-center px-6 py-12">
    <div class="max-w-xl w-full bg-slate-900/70 border border-slate-800 rounded-2xl p-8 backdrop-blur shadow-2xl space-y-6">
      <div class="space-y-2 text-center">
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold bg-emerald-950/80 text-emerald-300 border border-emerald-800/50">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          Autonomous 8-Agent Backend Engine
        </div>
        <h1 class="text-2xl font-black text-white tracking-tight">Backend Service Online</h1>
        <p class="text-xs text-slate-400 max-w-md mx-auto leading-relaxed">
          High-performance legal reasoning platform enforcing Islamic inheritance law (Faraizi) and Pakistan's WPRA 2020.
        </p>
      </div>

      <!-- Quick Metrics Grid -->
      <div class="grid grid-cols-2 gap-3 text-xs">
        <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800/80 space-y-1">
          <span class="text-[10px] uppercase font-bold text-slate-400">Primary AI Model</span>
          <div class="font-mono text-[11px] text-teal-300 truncate">{primary_model}</div>
        </div>
        <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800/80 space-y-1">
          <span class="text-[10px] uppercase font-bold text-slate-400">Groq Key Pool</span>
          <div class="font-mono text-[11px] text-emerald-300">{keys_count} API Keys Active</div>
        </div>
        <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800/80 space-y-1">
          <span class="text-[10px] uppercase font-bold text-slate-400">Math Accuracy</span>
          <div class="font-mono text-[11px] text-amber-300">Exact Fractions (1.0 Closure)</div>
        </div>
        <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800/80 space-y-1">
          <span class="text-[10px] uppercase font-bold text-slate-400">Live Streaming</span>
          <div class="font-mono text-[11px] text-sky-300">SSE Event Stream Active</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="space-y-2 pt-2">
        <a href="https://haqdar-app-iota.vercel.app" target="_blank" class="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-teal-600 to-teal-700 hover:from-teal-500 hover:to-teal-600 text-white font-bold text-xs shadow-lg shadow-teal-900/40 transition-all">
          <span>🚀 Open Main Web Application</span>
          <span class="text-[10px] font-mono text-teal-200">→</span>
        </a>
        <div class="grid grid-cols-2 gap-2">
          <a href="/docs" class="flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs border border-slate-700 transition-colors">
            <span>📖 Swagger Docs</span>
          </a>
          <a href="/health" class="flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs border border-slate-700 transition-colors">
            <span>🩺 Health JSON</span>
          </a>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-900 px-6 py-4 text-center text-[11px] text-slate-400">
    HaqDar (حقدار) • HEC × PakAngels National AI Hackathon • 2026
  </footer>
</body>
</html>"""

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
