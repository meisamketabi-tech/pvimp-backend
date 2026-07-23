
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog



def create_audit(
db:Session,
user_id:int,
action:str,
entity:str,
entity_id:int,
description:str=None
):

    log=AuditLog(

        user_id=user_id,

        action=action,

        entity=entity,

        entity_id=entity_id,

        description=description

    )


    db.add(log)

    db.commit()

    return log
