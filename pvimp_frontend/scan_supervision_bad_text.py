from pathlib import Path
import re
import json


BASE = Path("src/pages/Supervision")

RESULT = Path("supervision_bad_text_report.json")


patterns = [
    r"\?{2,}",
    r" +",
]


report = {}


for file in BASE.glob("*.tsx"):

    content = file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    lines = content.splitlines()

    matches = []

    for index, line in enumerate(lines, start=1):

        for pattern in patterns:

            if re.search(pattern, line):

                matches.append(
                    {
                        "line": index,
                        "text": line.strip()
                    }
                )

                break


    if matches:
        report[file.name] = matches


RESULT.write_text(
    json.dumps(
        report,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print("DONE")
print("Files with bad text:", len(report))
print("Report:", RESULT)