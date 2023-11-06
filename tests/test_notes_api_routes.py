from .test_main import testClient, test_engine
from database.base import  Base

def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)

def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=test_engine)

def test_create_note():
    response = testClient.post(
        "/notes/", json={
                "title": "pytest note title",
                "content": "pytest note Content"
            }
    )
    assert response.status_code == 200
    data = response.json() 
    assert data['title'] == 'pytest note title'
    assert data['content'] == 'pytest note Content'

def test_get_all_notes():
    response = testClient.get("/notes/all")
    assert response.status_code == 200

def test_get_note():
    response = testClient.get("/notes/1")
    assert response.status_code == 200
    data = response.json() 
    assert data['id'] == 1
    assert data['title'] == 'pytest note title'
    assert data['content'] == 'pytest note Content'

def test_update_get_note():
    response = testClient.put("/notes/1", json={
                "title": "pytest note title updated",
                "content": "pytest note Content updated"
            })
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'pytest note title updated'
    assert data['content'] == 'pytest note Content updated'

def test_delete_a_note():
    response = testClient.delete("/notes/1")
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Note deleted successfully'