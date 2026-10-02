#!/bin/bash
set -e

echo "============================================="
echo "   HaqDar (حقدار) - Multi-Agent AI Platform  "
echo "============================================="

# 1. Start FastAPI Backend
echo "[1/2] Starting FastAPI Backend on http://localhost:8000 ..."
cd /home/ilyan/og/backend
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 2. Start Next.js Frontend
echo "[2/2] Starting Next.js Frontend on http://localhost:3000 ..."
cd /home/ilyan/og/frontend
npm run dev &
FRONTEND_PID=$!

echo "Both services started successfully!"
echo "Backend:  http://localhost:8000 (API Docs at /docs)"
echo "Frontend: http://localhost:3000"

# Graceful termination
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
