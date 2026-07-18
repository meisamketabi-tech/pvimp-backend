from typing import List, Optional

from pydantic import BaseModel


class OrganizationTreeNode(BaseModel):

    id: int
    name: str
    code: str

    type_id: Optional[int] = None
    level_id: Optional[int] = None

    children: List["OrganizationTreeNode"] = []


OrganizationTreeNode.model_rebuild()
