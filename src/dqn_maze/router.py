from fastapi import APIRouter

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
