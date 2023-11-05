from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import Request
from sqlalchemy.orm import Session
from database.base import get_db
from database.models import Note
from .schema import NoteCreate, NoteUpdate

notes_router = APIRouter()

@notes_router.get("/notes/all")
async def read_notes(limit: int = Query(10, ge=1, le=100), 
                     offset: int = Query(0, ge=0), 
                     db: Session = Depends(get_db)):
    notes = db.query(Note).offset(offset).limit(limit).all()
    return notes


@notes_router.get("/notes/{note_id}")
async def read_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note


@notes_router.post("/notes/", response_model=NoteCreate)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**note.model_dump())  # Convert Pydantic model to SQLAlchemy model
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@notes_router.put("/notes/{note_id}", response_model=NoteUpdate)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    existing_note = db.query(Note).filter(Note.id == note_id).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in note_update.model_dump().items():
        setattr(existing_note, key, value)

    db.commit()
    db.refresh(existing_note)

    return note_update

@notes_router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}