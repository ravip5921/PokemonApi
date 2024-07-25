from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from database import get_async_session 
import models, schemas
from typing import List

router = APIRouter()

@router.get("/pokemons", response_model=List[schemas.Pokemon])
async def get_pokemons(
    name: str = None,
    type: str = None
):
    try:
        async for session in get_async_session():
            async with session.begin():
                query = select(models.Pokemon, models.Type).join(models.Pokemon.types)
                
                if name:
                    query = query.filter(models.Pokemon.name.ilike(f"%{name}%"))
                    
                if type:
                    query = query.filter(models.Type.type_name.ilike(f"%{type}%"))

                result = await session.execute(query)
                pokemons_with_types = result.fetchall()
                # print(pokemons_with_types)

                pokemons = {}
                for pokemon, type_data in pokemons_with_types:
                    pokemon_id = pokemon.id
                    pokemon_name = pokemon.name
                    pokemon_image_url = pokemon.image_url
                    type_id = type_data.id
                    type_name = type_data.type_name

                    if pokemon_id not in pokemons:
                        pokemons[pokemon_id] = {
                            "id": pokemon_id,
                            "name": pokemon_name,
                            "image_url": pokemon_image_url,
                            "types": []  # Initialize types as an empty list
                        }

                    pokemons[pokemon_id]["types"].append({"id": type_id, "type_name": type_name})

                # print(pokemons)

                # Convert dictionaries to schemas.Pokemon objects
                pokemon_objects = [schemas.Pokemon(**pokemon) for pokemon in pokemons.values()]
                return pokemon_objects

    except HTTPException as e:
        print(f"HTTPException occurred: {e}")