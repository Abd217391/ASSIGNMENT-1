from pydantic import BaseModel, EmailStr, Field


from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str 
