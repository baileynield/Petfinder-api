from sqlmodel import SQLModel, Field, Relationship
from typing import List


class UserAnimalLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="userinfo.id", primary_key=True)
    animal_id: int = Field(foreign_key="animal.id", primary_key=True)

class UserInfo(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str

    # Relationship with animals favorited by user
    favorites: List["Animal"] = Relationship(back_populates="favorited_by", link_model=UserAnimalLink)


class Animal(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
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
    
    # Relationship with users who favorited this animal
    favorited_by: List["UserInfo"] = Relationship(back_populates="favorites", link_model=UserAnimalLink)
