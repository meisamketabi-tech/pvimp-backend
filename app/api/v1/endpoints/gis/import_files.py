from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.gis.disease_occurrence_import import (
    import_disease_occurrences,
)
from app.services.gis.disease_report_import import (
    import_disease_reports,
)
from app.services.gis.epidemiology_import import (
    import_epidemiology_units,
)
from app.services.gis.laboratory_result_import import (
    import_laboratory_result,
)
from app.services.gis.send_sample_detail_import import (
    import_send_sample_detail,
)
from app.services.gis.slaughter_disposal_import import (
    import_slaughter_disposal,
)
from app.services.gis.spraying_import import (
    import_spraying,
)
from app.services.gis.surveillance_import import (
    import_surveillance,
)
from app.services.gis.vaccination_performance_import import (
    import_vaccination_performance,
)
from app.services.gis.vaccine_distribution_import import (
    import_vaccine_distribution,
)
from app.services.gis.vaccine_disposal_import import (
    import_vaccine_disposal,
)
from app.services.gis.vaccine_inventory_import import (
    import_vaccine_inventory,
)

# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/gis/import/disease-control",
    tags=["GIS Disease Control Import"],
)


# =========================================================
# Configuration
# =========================================================

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
    "epidemiology_units": "واحدهای اپیدمیولوژیک",
    "vaccination_performance": "عملکرد واکسیناسیون",
    "vaccine_distribution": "توزیع واکسن",
    "vaccine_disposal": "معدوم‌سازی واکسن",
    "vaccine_inventory": "موجودی واکسن",
}


Importer = Callable[
    ...,
    dict[str, Any],
]


IMPORT_SERVICES: dict[
    str,
    Importer,
] = {
    "epidemiology_units": import_epidemiology_units,
    "spraying": import_spraying,
    "disease_occurrence": import_disease_occurrences,
    "disease_report": import_disease_reports,
    "slaughter_disposal": import_slaughter_disposal,
    "laboratory_result": import_laboratory_result,
    "send_sample_detail": import_send_sample_detail,
    "surveillance": import_surveillance,
    "vaccination_performance": import_vaccination_performance,
    "vaccine_distribution": import_vaccine_distribution,
    "vaccine_disposal": import_vaccine_disposal,
    "vaccine_inventory": import_vaccine_inventory,
}


# =========================================================
# Result normalization
# =========================================================


def normalize_warnings(
    value: Any,
) -> list[str]:
    """
    Always return warnings as list[str].
    """

    if not value:
        return []

    if not isinstance(value, list):
        value = [value]

    normalized: list[str] = []

    for item in value:

        if item is None:
            continue

        if isinstance(item, str):
            normalized.append(item)
            continue

        if isinstance(item, dict):

            message = item.get("message")

            if message:
                normalized.append(str(message))
                continue

            warning_type = item.get("type")

            row = item.get("row")

            if warning_type and row:
                normalized.append(f"{warning_type} - ردیف {row}")
                continue

            if warning_type:
                normalized.append(str(warning_type))
                continue

            normalized.append("هشدار نامشخص")
            continue

        normalized.append(str(item))

    return normalized


def normalize_missing_units(
    value: Any,
) -> list[Any]:
    """
    Always return missing units as list.
    """

    if not value:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return list(value.values())

    return [value]


def normalize_import_result(
    result: Any,
) -> dict[str, Any]:
    """
    Normalize all importer results
    into one common structure.
    """

    if not isinstance(result, dict):
        result = {}

    try:
        inserted = int(result.get("inserted") or 0)
    except (TypeError, ValueError):
        inserted = 0

    try:
        skipped = int(result.get("skipped") or 0)
    except (TypeError, ValueError):
        skipped = 0

    try:
        failed = int(result.get("failed") or 0)
    except (TypeError, ValueError):
        failed = 0

    missing_units = (
        result.get("missing_units") or result.get("missing_epidemiology_units") or []
    )

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "missing_units": normalize_missing_units(missing_units),
        "warnings": normalize_warnings(result.get("warnings")),
    }


# =========================================================
# File helpers
# =========================================================


def save_file(
    file: UploadFile,
    folder: str,
) -> dict[str, Any]:

    upload_dir = BASE_DIR / folder

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    original_filename = file.filename or "uploaded_file.xlsx"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filename = f"{timestamp}_{original_filename}"

    path = upload_dir / filename

    try:

        with open(
            path,
            "wb",
        ) as destination:

            while True:

                chunk = file.file.read(1024 * 1024)

                if not chunk:
                    break

                destination.write(chunk)

    except OSError as exc:

        raise HTTPException(
            status_code=500,
            detail=("ذخیره فایل با خطا مواجه شد: " f"{exc}"),
        ) from exc

    return {
        "status": "success",
        "message": "فایل با موفقیت آپلود شد.",
        "department": "disease-control",
        "form": folder,
        "filename": filename,
        "path": str(path),
    }


def get_latest_file(
    folder_name: str,
) -> Path | None:

    folder = BASE_DIR / folder_name

    if not folder.exists():
        return None

    files = [
        file
        for file in folder.iterdir()
        if (file.is_file() and file.suffix.lower() in {".xlsx", ".xls"})
    ]

    if not files:
        return None

    return max(
        files,
        key=lambda file: file.stat().st_mtime,
    )


# =========================================================
# Upload
# =========================================================


@router.post("/upload")
async def upload(
    code: str = Form(...),
    file: UploadFile = File(...),
):
    if code not in FORMS:

        raise HTTPException(
            status_code=400,
            detail="Invalid form code.",
        )

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="نام فایل مشخص نیست.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in {
        ".xlsx",
        ".xls",
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "فرمت فایل مجاز نیست. "
                "فقط فایل Excel با پسوند "
                ".xlsx یا .xls قابل قبول است."
            ),
        )

    return save_file(
        file=file,
        folder=FORMS[code],
    )


# =========================================================
# Execute importer
# =========================================================


def execute_import(
    *,
    db: Session,
    form_key: str,
) -> dict[str, Any]:

    # -----------------------------------------------------
    # Validate form
    # -----------------------------------------------------

    if form_key not in FORMS:

        raise HTTPException(
            status_code=400,
            detail="Invalid form code.",
        )

    # -----------------------------------------------------
    # Find importer
    # -----------------------------------------------------

    importer = IMPORT_SERVICES.get(form_key)

    if importer is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Importer فرم "
                f"«{FORM_RESPONSE[form_key]}» "
                "هنوز پیاده‌سازی نشده است."
            ),
        )

    # -----------------------------------------------------
    # Find latest file
    # -----------------------------------------------------

    folder = FORMS[form_key]

    latest = get_latest_file(folder)

    if latest is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"برای فرم "
                f"«{FORM_RESPONSE[form_key]}» "
                "هیچ فایل Excel آپلود نشده است."
            ),
        )

    # -----------------------------------------------------
    # Execute importer
    # -----------------------------------------------------

    try:

        raw_result = importer(
            db=db,
            file_path=str(latest),
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                f"Import فرم " f"«{FORM_RESPONSE[form_key]}» " f"با خطا مواجه شد: {exc}"
            ),
        ) from exc

    # -----------------------------------------------------
    # Normalize result
    # -----------------------------------------------------

    result = normalize_import_result(raw_result)

    inserted = result["inserted"]

    skipped = result["skipped"]

    failed = result["failed"]

    missing_units = result["missing_units"]

    warnings = result["warnings"]

    # -----------------------------------------------------
    # Determine status
    # -----------------------------------------------------

    if missing_units:

        status = "warning"

        message = (
            f"تعدادی از رکوردهای فرم "
            f"«{FORM_RESPONSE[form_key]}» "
            "به دلیل ثبت نبودن واحد "
            "اپیدمیولوژیک وارد سیستم نشدند."
        )

        warnings.append(
            "برای ورود این رکوردها ابتدا "
            "واحدهای اپیدمیولوژیک موردنظر "
            "را از قسمت «واحدهای اپیدمیولوژیک» "
            "ثبت کنید."
        )

    elif failed > 0:

        status = "warning"

        message = (
            f"پردازش فرم " f"«{FORM_RESPONSE[form_key]}» " "با خطا یا هشدار همراه بود."
        )

    else:

        status = "success"

        message = f"فرم " f"«{FORM_RESPONSE[form_key]}» " "با موفقیت پردازش شد."

    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------

    return {
        "status": status,
        "message": message,
        "form": FORM_RESPONSE[form_key],
        "file": latest.name,
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "missing_units": missing_units,
        "warnings": warnings,
    }


# =========================================================
# Import endpoints
# =========================================================


@router.post("/epidemiology_units/import")
def epidemiology_units_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="epidemiology_units",
    )


@router.post("/spraying/import")
def spraying_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="spraying",
    )


@router.post("/disease_occurrence/import")
def disease_occurrence_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="disease_occurrence",
    )


@router.post("/disease_report/import")
def disease_report_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="disease_report",
    )


@router.post("/slaughter_disposal/import")
def slaughter_disposal_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="slaughter_disposal",
    )


@router.post("/laboratory_result/import")
def laboratory_result_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="laboratory_result",
    )


@router.post("/send_sample_detail/import")
def send_sample_detail_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="send_sample_detail",
    )


@router.post("/surveillance/import")
def surveillance_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="surveillance",
    )


@router.post("/vaccination_performance/import")
def vaccination_performance_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="vaccination_performance",
    )


@router.post("/vaccine_distribution/import")
def vaccine_distribution_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="vaccine_distribution",
    )


@router.post("/vaccine_disposal/import")
def vaccine_disposal_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="vaccine_disposal",
    )


@router.post("/vaccine_inventory/import")
def vaccine_inventory_import(
    db: Session = Depends(get_db),
):
    return execute_import(
        db=db,
        form_key="vaccine_inventory",
    )


# =========================================================
# Operation History
# =========================================================


@router.post("/operation_history/import")
def operation_history_import():

    return {
        "status": "warning",
        "message": (
            "Importer فرم " "«سابقه عملیات در واحد دامی» " "هنوز پیاده‌سازی نشده است."
        ),
        "form": ("سابقه عملیات در واحد دامی"),
        "file": None,
        "inserted": 0,
        "skipped": 0,
        "failed": 0,
        "missing_units": [],
        "warnings": [],
    }


# =========================================================
# Uploaded files
# =========================================================


@router.get("/files")
def get_uploaded_files():

    result: list[dict[str, Any]] = []

    for code, folder in FORMS.items():

        latest = get_latest_file(folder)

        if latest is None:

            result.append(
                {
                    "code": code,
                    "form": FORM_RESPONSE.get(
                        code,
                        code,
                    ),
                    "filename": None,
                    "size": 0,
                    "uploaded_at": None,
                }
            )

            continue

        stat = latest.stat()

        result.append(
            {
                "code": code,
                "form": FORM_RESPONSE.get(
                    code,
                    code,
                ),
                "filename": latest.name,
                "size": stat.st_size,
                "uploaded_at": (datetime.fromtimestamp(stat.st_mtime).isoformat()),
            }
        )

    return result
