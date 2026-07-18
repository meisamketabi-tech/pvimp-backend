from datetime import datetime


def generate_inspection_number():

    return (
        "INSP-"
        +
        datetime.utcnow()
        .strftime("%Y%m%d%H%M%S")
    )