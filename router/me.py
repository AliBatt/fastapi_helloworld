import fastapi
from fastapi import Depends

from app.deps import get_current_user
from app.schemas import UserOut
from app.user_model import User

router = fastapi.APIRouter()


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "message": "Profile fetched successfully",
        "data": UserOut.model_validate(current_user).model_dump(),
    }


@router.get("/user_profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return await get_profile(current_user)
