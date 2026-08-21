from pathlib import Path

import pandas as pd


def preview_excel(
    file_path: str,
    limit: int = 50,
) -> dict:

    path = Path(file_path)

    dataframe = pd.read_excel(path)

    dataframe = dataframe.head(limit)

    return {
        "columns": dataframe.columns.tolist(),
        "rows": dataframe.fillna("").to_dict(orient="records"),
        "count": len(dataframe),
    }
