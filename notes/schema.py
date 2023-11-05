from typing import Optional
from pydantic import BaseModel

class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]