from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from router import auth, me, posts, users_route


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="FastAPI User Management", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, tags=["Auth"])
app.include_router(me.router, tags=["Profile"])
app.include_router(users_route.router, tags=["Users"])
app.include_router(posts.router, tags=["Posts"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def read_root():
    return {"message": "Hello, World!", "docs": "/docs"}
