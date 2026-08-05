from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db
from app.services.gis.epidemiology_import import import_epidemiology_units

from fastapi import APIRouter, File, UploadFile, Form
from pathlib import Path
from datetime import datetime

router = APIRouter(
    prefix="/gis/import/disease-control", tags=["GIS Disease Control Import"]
)


BASE_DIR = Path("uploads/gis/disease-control")


FORMS = {
    "operation_history": "operation-history",
    "spraying": "spraying",
    "slaughter_disposal": "slaughter-disposal",
    "laboratory_result": "laboratory-result",
    "send_sample_detail": "send-sample-detail",
    "disease_occurrence": "disease-occurrence",
    "surveillance": "surveillance",
    "disease_report": "disease-report",
    "epidemiology_units": "epidemiology-units",
    "vaccination_performance": "vaccination-performance",
    "vaccine_distribution": "vaccine-distribution",
    "vaccine_disposal": "vaccine-disposal",
    "vaccine_inventory": "vaccine-inventory",
}


FORM_RESPONSE = {
    "operation_history": "سابقه عملیات در واحد دامی",
    "spraying": "مبارزه با انگل‌ها",
    "slaughter_disposal": "کشتار و معدوم سازی",
    "laboratory_result": "ثبت جواب آزمایش",
    "send_sample_detail": "ارسال نمونه",
    "disease_occurrence": "بروز بیماری",
    "surveillance": "پایش و مراقبت",
    "disease_report": "گزارش بیماری",
    "epidemiology_units": "اپیدمیولوژیک دام",
    "vaccination_performance": "عملکرد واکسیناسیون دام",
    "vaccine_distribution": "توزیع واکسن",
    "vaccine_disposal": "معدوم سازی واکسن دام",
    "vaccine_inventory": "وضعیت موجودی واکسن دام",
}


def save_file(file: UploadFile, folder: str):

    upload_dir = BASE_DIR / folder

    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename

    path = upload_dir / filename

    content = file.file.read()

    with open(path, "wb") as f:
        f.write(content)

    return {
        "status": "success",
        "department": "disease-control",
        "form": folder,
        "filename": filename,
        "path": str(path),
    }


@router.post("/upload")
async def upload(code: str = Form(...), file: UploadFile = File(...)):

    if code not in FORMS:
        return {"status": "error", "message": "invalid form code"}

    return save_file(file, FORMS[code])


@router.post("/epidemiology-units/import")
def import_epidemiology_units_endpoint(
    db: Session = Depends(get_db),
):

    folder = BASE_DIR / "epidemiology-units"

    if not folder.exists():
        return {
            "status": "error",
            "message": "No uploaded file found.",
        }

    files = list(folder.glob("*"))

    if not files:
        return {
            "status": "error",
            "message": "No uploaded file found.",
        }

    latest = max(
        files,
        key=lambda x: x.stat().st_mtime,
    )

    result = import_epidemiology_units(
        db,
        str(latest),
    )

    return {
        "status": "success",
        "file": latest.name,
        "result": result,
    }


@router.get("/files")
def get_uploaded_files():

    result = []

    for code, folder_name in FORMS.items():

        folder = BASE_DIR / folder_name

        latest = None

        if folder.exists():

            files = list(folder.glob("*"))

            if files:

                latest = max(files, key=lambda x: x.stat().st_mtime)

        if latest:

            stat = latest.stat()

            result.append(
                {
                    "form": FORM_RESPONSE[code],
                    "filename": latest.name,
                    "size": stat.st_size,
                    "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

        else:

            result.append(
                {
                    "form": FORM_RESPONSE.get(code, code),
                    "code": code,
                    "filename": None,
                    "size": 0,
                    "uploaded_at": None,
                }
            )

    return result
