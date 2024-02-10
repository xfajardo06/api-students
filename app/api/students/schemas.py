from pydantic import BaseModel


class SchemaStudentCreated(BaseModel):
    name: str
    semester: str

class SchemaStudentInscription(BaseModel):
    subject_codes: list
