from pydantic import BaseModel
from typing import Optional


class SchemaStudentCreated(BaseModel):
    name: str
    semester: str
    credits: Optional[int] = 100

class SchemaStudentInscription(BaseModel):
    subject_codes: list
