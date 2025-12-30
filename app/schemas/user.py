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

from typing import Optional

class UpdateProfile(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from pydantic import BaseModel
from datetime import datetime

class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    createdat: datetime   
    class Config:
        from_attributes = True  
