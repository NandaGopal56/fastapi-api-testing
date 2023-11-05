from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List

class NoteSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    modified_at: datetime

class NotesList(BaseModel):
    notes: List[NoteSchema]

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]