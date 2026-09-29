import asyncio
from datetime import datetime

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.schemas import UserLogin, UserOut, UserRegister
from app.user_model import User

router = fastapi.APIRouter()


async def _authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == email))
    db_user = result.scalar_one_or_none()

    password_ok = await asyncio.to_thread(
        verify_password, password, db_user.hashed_password
    ) if db_user else False

    if not db_user or not password_ok:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


def _login_response(db_user: User) -> dict:
    token = create_access_token({"sub": db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "data": UserOut.model_validate(db_user).model_dump(),
    }


@router.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = await asyncio.to_thread(hash_password, user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "data": UserOut.model_validate(new_user).model_dump(),
    }


@router.post("/signup")
async def signup(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await register(user, db)


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await _authenticate_user(user.email, user.password, db)
    return _login_response(db_user)


@router.post("/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    db_user = await _authenticate_user(form_data.username, form_data.password, db)
    return _login_response(db_user)
