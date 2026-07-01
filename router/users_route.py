import fastapi
from sqlalchemy.orm import Session
from app.database import get_db
from app.user_model import User
from fastapi import Depends

router = fastapi.APIRouter()
@router.get("/users")
async def get_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "data": [
            {
                "id": user.id,
                "email": user.email,
                "language": user.language
            }
            for user in users
        ]
    }
