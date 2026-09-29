import fastapi
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.post_model import Post
from app.schemas import CreatePost
from app.user_model import User

router = fastapi.APIRouter()


@router.post("/create-post")
async def create_post(
    post: CreatePost,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(title=post.title, content=post.content, author_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return {"message": "Post created successfully", "data": new_post}


@router.get("/get-posts")
async def get_posts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Post).where(Post.author_id == current_user.id))
    posts = result.scalars().all()
    return {"message": "Posts fetched successfully", "data": posts}
