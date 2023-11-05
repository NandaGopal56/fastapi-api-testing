from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy.orm import Session
from database.base import get_db
from database.models import Note
from .schema import NoteCreate

notes_router = APIRouter()

@notes_router.get("/", status_code=200)
async def Home(request: Request):
    return 'Welcome to the Notes App'

@notes_router.get("/notes/")
async def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@notes_router.post("/create_note/", response_model=NoteCreate)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**note.model_dump())  # Convert Pydantic model to SQLAlchemy model
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note