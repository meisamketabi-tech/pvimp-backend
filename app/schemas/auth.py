from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    username: str | None = None


class UserMe(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    email: str | None = None
    mobile: str | None = None
    is_active: bool
    role: str | None = None
    roles: list[str] = []

    class Config:
        from_attributes = True
