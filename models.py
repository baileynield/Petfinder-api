from sqlmodel import Field, Relationship, SQLModel


class Organization(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    animals: list["Animal"] = Relationship(back_populates="organization")


class Animal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    organization_id: int = Field(foreign_key="organization.id")
    organization: Organization = Relationship(back_populates="animals")
    #type: str
    breed: str
    color: str
    age: int
    gender: str
    size: str
    name: str
    spayed_neutered: bool
    house_trained: bool
    declawed: bool
    special_needs: bool
    shots_current: bool

