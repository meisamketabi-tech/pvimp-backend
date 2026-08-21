from pathlib import Path

from fastapi import UploadFile


UPLOAD_DIR = Path("storage/gis_imports")


async def save_excel(
    file: UploadFile,
) -> Path:

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        buffer.write(await file.read())

    return destination
