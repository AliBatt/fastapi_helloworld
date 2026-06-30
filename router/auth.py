from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.user_model import User
from app.schemas import UserRegister, UserLogin
from app.auth import hash_password, verify_password, create_access_token
import fastapi
from datetime import datetime
router = fastapi.APIRouter()

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
        updated_at=datetime.now()
    )
    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "data": new_user}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer", "data": db_user}



