from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., example="user1")
    email: str = Field(..., example="user1@example.com")
    password: str = Field(..., example="password")
    
class UserUpdate(BaseModel):
    oldEmail: str = Field(..., example="olduser1@example.com")
    oldPassword: str = Field(..., example="password")
    newName: str = Field(..., example="user1")
    newEmail: str = Field(..., example="newuser1@example.com")
    newPassword: str = Field(..., example="newPassword")
    newRole: str = Field(..., example="user")
    
class UserAuthorize(BaseModel):
    email: str = Field(..., example="user1@example.com")
    password: str = Field(..., example="password")