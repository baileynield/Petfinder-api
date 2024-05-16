import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import responses
from sqlmodel import Session
from database import get_db

from main import app

# Create a test client using the TestClient provided by FastAPI
client = TestClient(app)

mock_obj = MagicMock()

# Define the side_effect function
def side_effect_function(arg):
    if arg == 'specific_argument':
        return 'specific_return_value'
    else:
        return 'default_return_value'

# Assign the side_effect function to the mock object
mock_obj.side_effect = side_effect_function



@pytest.fixture
def db_session():
    session = MagicMock(spec=Session)
    return session

@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(get_db)

def test_get_animals_bad_token():
    # Test if you need a new auth token
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code=401
        response = client.get("/animals")
        assert response.status_code == 401

def test_get_animal_good_token():
    # Test getting json with good token
    with patch('requests.get') as mock_get:
        sample_pet = {'id': 71642652, 'organization_id': 'CT178', 'url': 'https://www.petfinder.com/dog/maggie-number-70-71642652/ct/killingworth/labs4rescue-ct178/?referrer_id=19ef7a19-250f-41f5-ad19-4c17601780a5&utm_source=api&utm_medium=partnership&utm_content=19ef7a19-250f-41f5-ad19-4c17601780a5', 'type': 'Dog', 'species': 'Dog', 'breeds': {'primary': 'Black Labrador Retriever', 'secondary': None, 'mixed': True, 'unknown': False}, 'colors': {'primary': None, 'secondary': None, 'tertiary': None}, 'age': 'Adult', 'gender': 'Female', 'size': 'Large', 'coat': None, 'attributes': {'spayed_neutered': True, 'house_trained': True, 'declawed': None, 'special_needs': False, 'shots_current': True}, 'environment': {'children': None, 'dogs': True, 'cats': True}, 'tags': ['Friendly', 'Affectionate', 'Loyal', 'Gentle', 'Sweet', 'Kind', 'Loving'], 'name': 'Maggie #70', 'description': 'Meet Maggie #70, or Miracle Maggie, as her foster mom calls her! Rescued from a shelter, only an hour before...', 'organization_animal_id': '2024100', 'photos': [], 'primary_photo_cropped': {'small': 'https://dbw3zep4prcju.cloudfront.net/animal/bb508b7e-1fbb-486f-8cba-5f0a2924ec73/image/7eaa73b5-82ea-4d55-99a4-f47f37aee639.jpg?versionId=2QQaxs.GWeTAAsXMIlipfo6vOUVDfjdK&bust=1715623172&width=300', 'medium': 'https://dbw3zep4prcju.cloudfront.net/animal/bb508b7e-1fbb-486f-8cba-5f0a2924ec73/image/7eaa73b5-82ea-4d55-99a4-f47f37aee639.jpg?versionId=2QQaxs.GWeTAAsXMIlipfo6vOUVDfjdK&bust=1715623172&width=450', 'large': 'https://dbw3zep4prcju.cloudfront.net/animal/bb508b7e-1fbb-486f-8cba-5f0a2924ec73/image/7eaa73b5-82ea-4d55-99a4-f47f37aee639.jpg?versionId=2QQaxs.GWeTAAsXMIlipfo6vOUVDfjdK&bust=1715623172&width=600', 'full': 'https://dbw3zep4prcju.cloudfront.net/animal/bb508b7e-1fbb-486f-8cba-5f0a2924ec73/image/7eaa73b5-82ea-4d55-99a4-f47f37aee639.jpg?versionId=2QQaxs.GWeTAAsXMIlipfo6vOUVDfjdK&bust=1715623172'}, 'videos': [], 'status': 'adoptable', 'status_changed_at': '2024-05-13T18:02:16+0000', 'published_at': '2024-05-13T18:02:15+0000', 'distance': None, 'contact': {'email': 'shana.luzusky@labs4rescue.org', 'phone': None, 'address': {}}}
        sample_data = {"animals": [sample_pet]}
        # sample_data = {"animals": []}
        mock_get.return_value.json.return_value = sample_data
        mock_get.return_value.status_code=200
        response = client.get("/animals")
        assert response.status_code == 200
        for i in range(len(sample_data)):
            if sample_data["animals"][i]["id"] == sample_pet["id"]:
                break
        else:
            assert False
        a = response.json()
        print(a)

def test_add_favorite_no_user(db_session: MagicMock, override_get_db):
    # Test adding favorite animal with no user
    db_session.exec.return_value.first.return_value = None
    user_id = 20
    animal_id = 1234

    response = client.post(f"/users/{user_id}/favorites/{animal_id}")
    assert response.status_code == 404

def test_add_favorite_no_animal_id(db_session, override_get_db):
    db_session.exec.return_value.first.return_value = None
    user_id = 20
    animal_id = 1234

    response = client.post(f"/users/{user_id}/favorites/{animal_id}")
    assert response.status_code == 404

def test_add_favorite_good():
    favorite_animal = {
        ""
    }

def test_delete_favorite_no_user():
    pass

def test_delete_favorite_no_animal_id():
    pass

def test_get_favorite_no_user():
    pass

def test_get_favorite_no_link():
    pass

def test_get_favorite_good():
    pass