from app.core.database import engine, Base

from app.db.models.responsible_health import *
from app.db.models.audit_log import *


def init():

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":
    init()