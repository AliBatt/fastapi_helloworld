from fastapi import FastAPI, HTTPException
from router import users_route
from router import auth
from router import me
from router import posts
from app.database import engine, Base

app = FastAPI()
app.include_router(users_route.router)
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(posts.router)

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/")
def home():
    return {"status": "API running"}