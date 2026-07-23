from fastapi import APIRouter

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.get("/definitions")
def definitions():
    return []

@router.get("/instances")
def instances():
    return []

@router.post("/start")
def start(data: dict):
    return {"status": "started", "data": data}

@router.post("/transition")
def transition(data: dict):
    return {"status": "transitioned", "data": data}
