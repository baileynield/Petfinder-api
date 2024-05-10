### *** As of May 9th, 2024
from fastapi import Depends, FastAPI, HTTPException
from decouple import config
import requests
from sqlmodel import select, Session

from database import get_db
from models import Animal
from schemas import AnimalSchema


app = FastAPI()


base_url = "https://api.petfinder.com/v2"

AUTH_TOKEN = config('AUTH_TOKEN')

# Check if an animal with a specific ID exists in the database
def animal_exists(db: Session, animal_id: int) -> bool:
    statement = select(Animal).where(Animal.id == animal_id)
    existing_animal = db.exec(statement).first
    return existing_animal is not None


@app.get("/animals")
async def get_animals(db: Session = Depends(get_db)):
    headers = {
        "Authorization" : f"Bearer {AUTH_TOKEN}"
    }
    # Fetch the animals from the external API
    response = requests.get(url=f"{base_url}/animals", headers=headers)
    animals_data = response.json()

    # Loop through the animals and check if they exist in the database
    for animal_data in animals_data["animals"]:
        animal_id = animal_data["id"]

        # Check if the animal ID already exists in the database
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


# Check if an animal with a specific ID already exists
def animal_exists(db: Session, animal_id: int) -> bool:
    statement = select(Animal).where(Animal.id == animal_id)
## existing_animal = db.query(Animal).filter(Animal.id == animal_id).first() # Not for SQLModel
    existing_animal = db.exec(statement).first
    return existing_animal is not None

# POST endpoint to create a new animal
@app.post("/animals")
async def create_animal(
    new_animal: AnimalSchema,  # using schemas.py
    db: Session = Depends(get_db)
):
    # Check if the animal ID already exists in the database and raise error if it is
    if animal_exists(db, new_animal.id):
        raise HTTPException(
            status_code=400, detail=f"Animal with ID {new_animal.id} already exists."
        )

    # Create a new Animal object and add it to the database
    animal = Animal(
        id=new_animal.id,
        organization_id=new_animal.organization_id,
        type=new_animal.type,
        breed=new_animal.breed,
        color=new_animal.color,
        age=new_animal.age,
        gender=new_animal.gender,
        size=new_animal.size,
        spayed_neutered=new_animal.spayed_neutered,
        house_trained=new_animal.house_trained,
        declawed=new_animal.declawed,
        special_needs=new_animal.special_needs,
        shots_current=new_animal.shots_current,
        name=new_animal.name,
    )

    db.add(animal)
    db.commit()


@app.put("/animals/{animal_id}")
async def update_animal(animald_id: int, update_data: AnimalSchema, db: Session = Depends(get_db)):
    pass