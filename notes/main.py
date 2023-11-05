from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import Request
from sqlalchemy.orm import Session
from database.base import get_db
from database.models import Note
from exceptions.main import NotFoundError
from .schema import NoteSchema, NotesList, NoteCreate, NoteUpdate
from .db_operations import db_read_item, db_create_note, db_update_note, db_delete_note, db_read_all_items


notes_router = APIRouter()

@notes_router.get("/notes/all", response_model=NotesList)
async def get_all_notes(limit: int = Query(10, ge=1, le=100), 
                     offset: int = Query(0, ge=0), 
                     db: Session = Depends(get_db)):
    notes = db_read_all_items(limit, offset, db)
    return notes


@notes_router.get("/notes/{note_id}", response_model=NoteSchema)
async def get_a_note(note_id: int, db: Session = Depends(get_db)):
    try:
        note = db_read_item(note_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@notes_router.post("/notes/", response_model=NoteCreate)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = db_create_note(note, db)
    return new_note

@notes_router.put("/notes/{note_id}", response_model=NoteUpdate)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    try:
        updated_note = db_update_note(note_id, note_update, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")

    return updated_note

@notes_router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    try:
        status = db_delete_note(note_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return status