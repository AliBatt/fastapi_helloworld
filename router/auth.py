from datetime import datetime

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.schemas import UserLogin, UserRegister
from app.user_model import User

router = fastapi.APIRouter()


def _authenticate_user(email: str, password: str, db: Session) -> User:
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


def _login_response(db_user: User) -> dict:
    token = create_access_token({"sub": db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "data": {
            "id": db_user.id,
            "email": db_user.email,
            "language": db_user.language,
        },
    }


@router.post("/signup")
def signup(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        language=user.language,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "data": {
            "id": new_user.id,
            "email": new_user.email,
            "language": new_user.language,
        },
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = _authenticate_user(user.email, user.password, db)
    return _login_response(db_user)


@router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = _authenticate_user(form_data.username, form_data.password, db)
    return _login_response(db_user)
