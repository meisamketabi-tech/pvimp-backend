from fastapi import APIRouter, File, UploadFile
from pathlib import Path
from datetime import datetime

router = APIRouter(
    prefix="/gis/import/disease-control", tags=["GIS Disease Control Import"]
)


BASE_DIR = Path("uploads/gis/disease-control")


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


# فرم واحد اپیدمیولوژیک


@router.post("/epidemiology-units/upload")
async def upload_epidemiology_units(file: UploadFile = File(...)):

    return save_file(file, "epidemiology-units")


# فرم کانون بیماری


@router.post("/outbreak/upload")
async def upload_outbreak(file: UploadFile = File(...)):

    return save_file(file, "outbreak")


# فرم واکسیناسیون


@router.post("/vaccination/upload")
async def upload_vaccination(file: UploadFile = File(...)):

    return save_file(file, "vaccination")


# فرم مراقبت بیماری


@router.post("/surveillance/upload")
async def upload_surveillance(file: UploadFile = File(...)):

    return save_file(file, "surveillance")
