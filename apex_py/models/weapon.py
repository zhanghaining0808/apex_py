from sqlmodel import Field, SQLModel


class Weapon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str
    ammo: str
    Basic_magazine: int
