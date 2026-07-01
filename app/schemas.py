from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=64)
    language: str = "en"
    

class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str

