from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User

from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



@router.post(
    "/login",
    response_model=Token,
)
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )


    if not verify_password(
        password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )


    token = create_access_token(
        data={
            "sub": user.username
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "expires_in": 3600,

    }