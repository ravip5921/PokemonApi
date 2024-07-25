from pydantic import BaseModel
from typing import List, Optional

class PokemonBase(BaseModel):
    name: str
    image_url: Optional[str] = None

class PokemonCreate(PokemonBase):
    pass

class TypeBase(BaseModel):
    type_name: str

class Type(TypeBase):
    id: int  # Ensure id is present

    class Config:
        orm_mode = True

class Pokemon(PokemonBase):
    id: int
    types: List[Type]

    class Config:
        orm_mode = True


