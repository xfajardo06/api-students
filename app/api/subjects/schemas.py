from pydantic import BaseModel, Field

class SchemaFinishSubject(BaseModel):
    score: int = Field(..., ge=1, le=5)
