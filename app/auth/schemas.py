from pydantic import BaseModel, EmailStr, constr
from typing import Optional



class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserRegisterSchema(BaseModel):
    email: EmailStr
    name: constr(min_length=1, max_length=50)
    password: str
    phone: Optional[str] = ""