from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InspectionFilter(BaseModel):

    inspection_type_id: Optional[int] = None

    organization_unit_id: Optional[int] = None

    inspector_id: Optional[int] = None

    from_date: Optional[datetime] = None

    to_date: Optional[datetime] = None

    status: Optional[str] = None

    result: Optional[str] = None