import fastapi
from app.schemas import CreatePost
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends
from app.post_model import Post
from app.user_model import User
from router.me import get_current_user
from fastapi import HTTPException
from app.post_model import Post
router = fastapi.APIRouter()

@router.post("/create-post")
async def create_post(post: CreatePost, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    new_post = Post(title=post.title, content=post.content, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "data": new_post}

@router.get("/get-posts")
async def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.author_id == current_user.id).all()
    return {"message": "Posts fetched successfully", "data": posts}