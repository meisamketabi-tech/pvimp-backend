from pathlib import Path

BASE = Path("src/pages/Supervision")


TEXTS = {
    "SupervisionInspectionList.tsx": "لیست بازرسی‌ها",
    "SupervisionGISImport.tsx": "ورود اطلاعات GIS",
    "SupervisionGISDashboard.tsx": "داشبورد GIS نظارت",
    "SupervisionSamples.tsx": "نمونه‌برداری",
    "SupervisionLegal.tsx": "پرونده‌های قضایی",
}


def restore_text(path: Path, title: str):
    content = path.read_text(encoding="utf-8")

    replacements = [
        "???",
        "????",
        "??????",
    ]

    for bad in replacements:
        content = content.replace(bad, title)

    path.write_text(
        content,
        encoding="utf-8",
        newline="\n"
    )

    print("Fixed:", path.name)


for filename, text in TEXTS.items():

    file_path = BASE / filename

    if file_path.exists():
        restore_text(file_path, text)
    else:
        print("Missing:", filename)


print("DONE")