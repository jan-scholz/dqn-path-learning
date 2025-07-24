from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from dqn_maze.router import router

app = FastAPI()

app.include_router(router)

# Mount static frontend
webapp_dist_dir = Path(__file__).resolve().parent.parent / "webapp" / "dist"
app.mount("/", StaticFiles(directory=webapp_dist_dir, html=True), name="static")
