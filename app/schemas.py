from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    language: str = "en"
    

class UserLogin(BaseModel):
    email: str
    password: str