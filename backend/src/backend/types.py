from pydantic import BaseModel

class Document(BaseModel):
    text: str
    metadata: dict
    path: str