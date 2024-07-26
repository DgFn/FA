from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True


class CreateUserSchema(BaseModel):
    login: str
    password: str


class UpdateUserSchema(BaseModel):
    new_login: str


class AuthSchema(BaseModel):
    login: str
    password: str


