from typing import List, Optional

from pydantic import BaseModel


class OrganizationPositionNode(BaseModel):

    id: int
    name: str


class OrganizationUserNode(BaseModel):

    id: int
    username: str
    full_name: str
    role: str


class OrganizationTreeNode(BaseModel):

    id: int
    name: str
    code: str

    type_id: Optional[int] = None
    level_id: Optional[int] = None

    positions: List[OrganizationPositionNode] = []

    users: List[OrganizationUserNode] = []

    children: List["OrganizationTreeNode"] = []


OrganizationTreeNode.model_rebuild()