from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class OrganizationPositionTree(BaseModel):

    id: int
    position_id: int
    position_code: str
    position_title: str

    user_id: Optional[int] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class OrganizationTreeNode(BaseModel):

    id: int
    name: str
    code: str
    unit_type: str

    parent_id: Optional[int] = None

    positions: List[OrganizationPositionTree] = []

    children: List["OrganizationTreeNode"] = []

    model_config = ConfigDict(
        from_attributes=True
    )


OrganizationTreeNode.model_rebuild()
