from fastapi import APIRouter

router = APIRouter(prefix="/rules", tags=["Rules"])

@router.post("/validate")
def validate(data: dict):
    return {
        "valid": True,
        "errors": []
    }
