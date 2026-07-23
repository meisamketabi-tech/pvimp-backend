from fastapi import APIRouter

router = APIRouter(prefix="/dynamic-forms", tags=["Dynamic Forms"])

@router.get("/")
def list_forms():
    return []

@router.get("/{form_id}")
def get_form(form_id: int):
    return {"id": form_id}

@router.post("/save")
def save(data: dict):
    return {"saved": True}
