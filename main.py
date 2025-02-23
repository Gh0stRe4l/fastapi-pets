
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")  # Ruta en la raíz
def read_root():
    return {"message": "Welcome to the Pet API!"}

@app.get("/pets")  # Endpoint correcto
def get_pets():
    return {"message": "List of pets"}

# Pet model
class Pet(BaseModel):
    id_pet: int
    name: str
    age: int


# In-memory database (list)
pets_db: List[Pet] = []


# Create a new pet
@app.post("/pets/", response_model=Pet)
def create_pet(pet: Pet):
    for existing_pet in pets_db:
        if existing_pet.id_pet == pet.id_pet:
            raise HTTPException(status_code=400, detail="Pet ID already exists")

    pets_db.append(pet)
    return pet


# List all pets
@app.get("/pets/", response_model=List[Pet])
def list_pets():
    return pets_db


# Get a pet by ID
@app.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    for pet in pets_db:
        if pet.id_pet == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")


# Update a pet
@app.put("/pets/{pet_id}", response_model=Pet)
def update_pet(pet_id: int, updated_pet: Pet):
    for index, pet in enumerate(pets_db):
        if pet.id_pet == pet_id:
            pets_db[index] = updated_pet
            return updated_pet
    raise HTTPException(status_code=404, detail="Pet not found")


# Delete a pet
@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    for index, pet in enumerate(pets_db):
        if pet.id_pet == pet_id:
            del pets_db[index]
            return {"message": "Pet successfully deleted"}
    raise HTTPException(status_code=404, detail="Pet not found")


# Calculate pet age percentage based on a maximum age
@app.get("/pets/{pet_id}/age-percentage")
def age_percentage(pet_id: int, max_age: int):
    for pet in pets_db:
        if pet.id_pet == pet_id:
            percentage = (pet.age / max_age) * 100
            return {"id_pet": pet.id_pet, "name": pet.name, "age_percentage": f"{percentage:.2f}%"}
    raise HTTPException(status_code=404, detail="Pet not found")

