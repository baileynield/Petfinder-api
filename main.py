from fastapi import FastAPI
from decouple import config
import requests


app = FastAPI()


base_url = "https://api.petfinder.com/v2"

AUTH_TOKEN = config('AUTH_TOKEN')


@app.get("/animals")
async def get_animals():
    headers = {
        "Authorization" : f"Bearer {AUTH_TOKEN}"
    }
    response = requests.get(url=f"{base_url}/animals", headers=headers)
    return response.json()

@app.get("/animals/{animal_species}")
async def get_animal_type(animal_species: str):
    headers = {
        "Authorization" : f"Bearer {AUTH_TOKEN}"
    }
    response = requests.get(url=f"{base_url}/animals/{animal_species}", headers=headers)
    animal_detail = response.json()