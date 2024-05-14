import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main4 import app

# Create a test client using the TestClient provided by FastAPI
client = TestClient(app)

# def test_create_user():
#     # Test creating a new user
#     response = client.post("/users", json={"id": 10, "name": "Test User"})
#     assert response.status_code == 200
#     assert response.json() == 10  # Assuming the response is the user ID

# def test_get_animals():
#     # Test getting animals
#     response = client.get("/animals")
#     assert response.status_code == 200

# def test_add_favorite():
#     # Test adding a favorite animal
#     response = client.post("/users/1/favorites/10")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Animal with ID 10 added to favorites."}

# def test_remove_favorite():
#     # Test removing a favorite animal
#     response = client.delete("/users/1/favorites/10")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Animal with ID 10 removed from favorites."}

# def test_get_user_favorites():
#     # Test getting user favorites
#     response = client.get("/users/1/favorites")
#     assert response.status_code == 200

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
        # sample_data = {"animals": [sample_pet]}
        sample_data = {"animals": []}
        mock_get.return_value.json.return_value == sample_data
        mock_get.return_value.status_code=200
        response = client.get("/animals")
        assert response.status_code == 200
        a = response.json()
        print(a)