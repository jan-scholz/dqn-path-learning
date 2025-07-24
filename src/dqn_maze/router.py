from fastapi import APIRouter, HTTPException

from dqn_maze.maze_environment import Maze
from dqn_maze.models import MazeInput

router = APIRouter()

shutdown_initiated = False


@router.on_event("startup")
async def start_event():
    print("[Router] Starting")


@router.get("/health")
async def health_check():
    return {"type": "status", "value": "ok"}


@router.on_event("shutdown")
async def shutdown_event():
    global shutdown_initiated
    if shutdown_initiated:
        return
    shutdown_initiated = True
    print("[Router] Shutdown initiated")


@router.post("/create_maze")
async def create_maze(data: MazeInput):
    maze = Maze()
    try:
        maze.from_str(data.maze)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid maze format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return {"rows": maze.rows, "cols": maze.cols, "grid": str(maze)}
