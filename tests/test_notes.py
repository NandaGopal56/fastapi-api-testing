from .test_main import testClient, test_engine
from database.base import  Base

def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)

def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=test_engine)

###############################################
#           TESTS
###############################################

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





