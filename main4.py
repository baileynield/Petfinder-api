### *** As of May 9th, 2024
from fastapi import Depends, FastAPI, HTTPException
from decouple import config
import requests
from sqlmodel import select, Session

from database import get_db
from models import Animal, UserInfo, UserAnimalLink
from schemas import UserCreate


app = FastAPI()


base_url = "https://api.petfinder.com/v2"

AUTH_TOKEN = config('AUTH_TOKEN')

# Create a new user and return the user ID
def create_user(db: Session, id: int, name: str) -> int:
    # Check if the user ID already exists
    existing_user = db.exec(select(UserInfo).where(UserInfo.id == id)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already exists")
    
    new_user = UserInfo(id=id, name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh the user instance to get the auto-generated user ID
    return new_user.id

@app.post("/users", response_model=int)
async def create_user_and_return_id(id: int, name: str, db: Session = Depends(get_db)):
    user_id = create_user(db, id, name)
    return user_id



# Check if an animal with a specific ID exists in the database
def animal_exists(db: Session, animal_id: int) -> bool:
    statement = select(Animal).where(Animal.id == animal_id)
    existing_animal = db.exec(statement).first()
    return existing_animal is not None


@app.get("/animals")
async def get_animals(db: Session = Depends(get_db)) -> list[Animal]:
    headers = {
        "Authorization" : f"Bearer {AUTH_TOKEN}"
    }
    # Fetch the animals from the external API
    response = requests.get(url=f"{base_url}/animals", headers=headers)
    animals_data = response.json()

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid Auth Token")

    # Loop through the animals and check if they exist in the database
    for animal_data in animals_data["animals"]:
        print("Animal Data:", animal_data)
        animal_id = animal_data["id"]
        
        if animal_id is None:
            continue


        # Check if the animal ID already exists in the database
        animal = None
        if not animal_exists(db, animal_id):
            animal = Animal(
                id=animal_id,
                organization_id=animal_data["organization_id"],
                type=animal_data["type"],
                breed=animal_data["breeds"]["primary"],
                color=animal_data["colors"]["primary"],
                age=animal_data["age"],
                gender=animal_data["gender"],
                size=animal_data["size"],
                spayed_neutered=animal_data["attributes"]["spayed_neutered"],
                house_trained=animal_data["attributes"]["house_trained"],
                declawed=animal_data["attributes"]["declawed"],
                special_needs=animal_data["attributes"]["special_needs"],
                shots_current=animal_data["attributes"]["shots_current"],
                name=animal_data["name"]
            )
            db.add(animal)
            db.commit()
        if animal:
            db.add(animal)
    db.commit()
    return db.exec(select(Animal)).all()



# Add an animal to a user's favorites
@app.post("/users/{user_id}/favorites/{animal_id}")
async def add_favorite(user_id: int, animal_id: int, db: Session = Depends(get_db)):

    user = db.exec(select(UserInfo).where(UserInfo.id == user_id)).first()
    animal = db.exec(select(Animal).where(Animal.id == animal_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found.")

    # Check if the relationship exists
    link = db.exec(select(UserAnimalLink).where(UserAnimalLink.user_id == user_id, UserAnimalLink.animal_id == animal_id)).first()

    if not link:
        # Add the relationship if it doesn't exist
        db.add(UserAnimalLink(user_id=user_id, animal_id=animal_id))
        db.commit()

    return {"message": f"Animal with ID {animal_id} added to favorites."}


# Remove an animal from a user's favorites
@app.delete("/users/{user_id}/favorites/{animal_id}")
async def remove_favorite(user_id: int, animal_id: int, db: Session = Depends(get_db)):
    user = db.exec(select(UserInfo).where(UserInfo.id == user_id)).first()
    animal = db.exec(select(Animal).where(Animal.id == animal_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found.")

    # Check for the existing relationship
    link = db.exec(select(UserAnimalLink).where(UserAnimalLink.user_id == user_id, UserAnimalLink.animal_id == animal_id)).first()

    if link:
        db.delete(link)  # Remove the relationship
        db.commit()

    return {"message": f"Animal with ID {animal_id} removed from favorites."}


# Get all favorite animals for a user
@app.get("/users/{user_id}/favorites")
async def get_user_favorites(user_id: int,db: Session = Depends(get_db)):
    # Check for user
    user = db.exec(select(UserInfo).where(UserInfo.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Get the relationships for favorite animals and user
    links = db.exec(select(UserAnimalLink).where(UserAnimalLink.user_id == user_id)).all()

    if not links:
        raise HTTPException(status_code=404, detail="No favorites found for this user.")

    # Get the animal IDs from the links and then query the animals
    animal_ids = [link.animal_id for link in links]

    animals = db.exec(select(Animal).where(Animal.id.in_(animal_ids))).all()

    return animals