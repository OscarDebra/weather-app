from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class DeleteUserRequest(BaseModel):
    username: str

class ChangePasswordRequest(BaseModel):
    username: str
    new_password: str