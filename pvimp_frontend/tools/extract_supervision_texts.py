from pathlib import Path
import re
import json


ROOT = Path(".")


files = list(ROOT.rglob("Supervision*.tsx"))

result = []


for file in files:

    text = file.read_text(
        encoding="utf-8",
        errors="ignore"
    )


    strings = re.findall(
        r'["\'`]([^"\'`]{2,80})["\'`]',
        text
    )


    for s in strings:

        if (
            any("\u0600" <= c <= "\u06ff" for c in s)
            or "????" in s
        ):
            result.append(
                {
                    "file": str(file),
                    "text": s
                }
            )


print("Files:", len(files))


Path(
    "supervision_texts_extract.json"
).write_text(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print("Extracted texts:", len(result))