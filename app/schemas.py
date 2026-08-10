from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str 
    language: str = "en"
    

class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str

class CreatePost(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    content: str = Field(min_length=5, max_length=255)
    author_id: int