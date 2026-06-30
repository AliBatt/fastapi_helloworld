from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}