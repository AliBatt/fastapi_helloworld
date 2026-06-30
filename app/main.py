from fastapi import FastAPI, HTTPException
from router import users_route

app = FastAPI()
app.include_router(users_route.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}