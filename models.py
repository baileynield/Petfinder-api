from sqlmodel import Field, SQLModel


class Animal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    organization_id: str | None
    type: str | None
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
    name: str | None