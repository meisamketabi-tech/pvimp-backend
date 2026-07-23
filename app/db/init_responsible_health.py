
from app.core.database import engine,Base

from app.models.responsible_health import *
from app.models.audit_log import *


def init():

    Base.metadata.create_all(
        bind=engine
    )


if __name__=="__main__":

    init()

