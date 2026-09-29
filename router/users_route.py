import asyncio
from datetime import datetime

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import hash_password
from app.database import get_db
from app.deps import get_current_user
from app.schemas import UserOut, UserUpdate
from app.user_model import User

router = fastapi.APIRouter()


@router.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {
        "message": "Users fetched successfully",
        "data": [UserOut.model_validate(user).model_dump() for user in users],
    }


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "User fetched successfully",
        "data": UserOut.model_validate(user).model_dump(),
    }


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    updates: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if updates.email and updates.email != user.email:
        existing_result = await db.execute(select(User).where(User.email == updates.email))
        if existing_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already in use")

    if updates.name is not None:
        user.name = updates.name
    if updates.email is not None:
        user.email = updates.email
    if updates.phone is not None:
        user.phone = updates.phone
    if updates.password is not None:
        user.hashed_password = await asyncio.to_thread(hash_password, updates.password)

    user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(user)

    return {
        "message": "User updated successfully",
        "data": UserOut.model_validate(user).model_dump(),
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully", "id": user_id}
