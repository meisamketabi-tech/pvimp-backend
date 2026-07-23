from fastapi import APIRouter, UploadFile, File, Form, Depends

from sqlalchemy.orm import Session

from pathlib import Path
import shutil

from app.core.database import get_db
from app.models.attachment import Attachment


router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"]
)


UPLOAD = Path(
    "uploads/health"
)

UPLOAD.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/")
def upload(
    entity_type: str = Form(...),
    entity_id: int = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    filename = file.filename

    path = UPLOAD / filename

    with path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    obj = Attachment(

        entity_type=entity_type,

        entity_id=entity_id,

        file_name=filename,

        file_path=str(path)

    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj



@router.get("/{entity}/{id}")
def get_files(
    entity: str,
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Attachment
    ).filter(
        Attachment.entity_type == entity,
        Attachment.entity_id == id
    ).all()