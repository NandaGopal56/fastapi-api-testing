from .test_main import testClient, test_engine, db_session
from database.base import  Base
from notes.db_operations import db_create_note, db_read_item, db_read_all_items, db_delete_note, db_update_note
from notes.schema import NoteCreate, NoteSchema, NotesList, NoteUpdate
import pytest

def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)

def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=test_engine)



###############################################
#           TESTS
###############################################

def test_db_operation_create_note(db_session):
    data = db_create_note(
        NoteCreate(title = "pytest note title", content = "pytest note Content"), db_session
    )
    assert data.title == 'pytest note title'
    assert data.content == 'pytest note Content'

def test_db_get_all_notes(db_session):
    data = db_read_all_items(1, 0, db_session)
    assert data.notes[0].title == 'pytest note title'
    assert data.notes[0].content == 'pytest note Content'

def test_db_get_a_note(db_session):
    data = db_read_item(1, db_session)
    assert data.title == 'pytest note title'
    assert data.content == 'pytest note Content'

def test_db_update_a_note(db_session):
    data = db_update_note(1, 
                NoteCreate(title = "pytest note title updated", content = "pytest note Content updated"), 
                db_session
            )
    assert data.title == 'pytest note title updated'
    assert data.content == 'pytest note Content updated'

def test_db_delete_a_note(db_session):
    response = db_delete_note(1, db_session)
    assert response['message'] == 'Note deleted successfully'