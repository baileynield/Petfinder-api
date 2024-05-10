from pydantic import BaseModel


class AnimalSchema(BaseModel):
    id: int
    organization_id: str
    type: str
    breed: str | None
    color: str | None
    age: str | None
    gender: str | None
    size: str | None
    spayed_neutered: bool | None
    house_trained: bool | None
    declawed: bool | None
    special_needs: bool | None
    shots_current: bool | None
    name: str
