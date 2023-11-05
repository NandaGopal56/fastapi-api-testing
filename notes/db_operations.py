from sqlalchemy.orm import Session
from .schema import NoteSchema, NotesList, NoteCreate, NoteUpdate
from exceptions.main import NotFoundError
from database.models import Note as Note
from pydantic import TypeAdapter
from typing import List

def db_find_note(note_id: int, db: Session) -> Note:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise NotFoundError("Note not found")
    return note

def db_read_all_items(limit, offset, db) -> List[NoteSchema]:
    notes = db.query(Note).offset(offset).limit(limit).all()
    notes = [NoteSchema(**note.__dict__) for note in notes]
    notes = NotesList(notes=notes)
    return notes

def db_read_item(note_id: int, db: Session) -> NoteSchema:
    note = db_find_note(note_id, db)
    return NoteSchema(**note.__dict__)

def db_create_note(note: NoteCreate, db: Session) -> NoteCreate:
    new_note = Note(**note.model_dump())  # Convert Pydantic model to SQLAlchemy model
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return NoteCreate(**new_note.__dict__)

def db_update_note(note_id: int, note_update: NoteUpdate, db: Session) -> NoteUpdate:
    existing_note = db.query(Note).filter(Note.id == note_id).first()

    if existing_note is None:
        raise NotFoundError("Note not found")

    for key, value in note_update.model_dump().items():
        setattr(existing_note, key, value)

    db.commit()
    db.refresh(existing_note)

    return NoteUpdate(**existing_note.__dict__)

def db_delete_note(note_id: int, db: Session):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise NotFoundError("Note not found")
    
    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}