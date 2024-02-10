from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, constr, SecretStr



class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserRegisterSchema(BaseModel):
    email: EmailStr
    name: constr(min_length=1, max_length=50)
    password: str