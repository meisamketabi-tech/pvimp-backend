from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.v1.endpoints.gis.disease_control_dashboard import _scope_for_user
from app.db.models.user import User
from app.services.gis_disease_control_ai_service import GISDiseaseControlAIService

router = APIRouter(prefix="/gis/disease-control-ai", tags=["GIS Disease Control AI"])


class AIQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@router.post("/ask")
def ask_ai(
    payload: AIQuestion,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    province_code, county_code = _scope_for_user(db, current_user, None, None)
    return GISDiseaseControlAIService.answer(
        db=db,
        question=payload.question,
        province_code=province_code,
        county_code=county_code,
    )
