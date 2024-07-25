import asyncio
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_async_session, engine, Base
from models import Pokemon, Type, PokemonType

import os
from dotenv import load_dotenv
import configparser

# Load environment variables from .env file
load_dotenv(dotenv_path='./config/.env')

config_path = os.getenv('CONFIG_PATH')
config = configparser.ConfigParser()
config.read(config_path)

BASE_URL = config.get('pokeapi', 'BASE_URL') + '?limit='+config.get('pokeapi', 'LIMIT')
TIMEOUT = config.getint('pokeapi', 'TIMEOUT')

# POKE API call to get a list of pokemons with limit = LIMIT
async def fetch_pokemon_list():
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

# POKE API Call to get data of individual pokemons
async def fetch_pokemon_types(semaphore, pokemon_url):
    async with semaphore:
        async with httpx.AsyncClient() as client:
            response = await client.get(pokemon_url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
async def process_pokemon(pokemon_list):
    semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for pokemon in pokemon_list['results']:
            tasks.append(fetch_pokemon_types(semaphore, pokemon['url']))
            print(pokemon['url'])
        responses = await asyncio.gather(*tasks)

    filtered_pokemon = []
    for pokemon, response in zip(pokemon_list['results'], responses):
        name = pokemon['name']
        pokemon_id = pokemon['url'].split('/')[-2]
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
        types = [t['type']['name'] for t in response['types']]
        
        filtered_pokemon.append({
            'name': name,
            'image_url': image_url,
            'types': types
        })
    
    return filtered_pokemon

async def insert_pokemon_data(session: AsyncSession, pokemon_data):
    for pkm in pokemon_data:
        pokemon = Pokemon(name=pkm['name'], image_url=pkm['image_url'])
        session.add(pokemon)
        await session.commit()
        await session.refresh(pokemon)
        
        for type_name in pkm['types']:
            stmt = select(Type).where(Type.type_name == type_name)
            result = await session.execute(stmt)
            type_instance = result.scalar_one_or_none()
            if not type_instance:
                type_instance = Type(type_name=type_name)
                session.add(type_instance)
                await session.commit()
                await session.refresh(type_instance)
            
            pokemon_type = PokemonType(pokemon_id=pokemon.id, type_id=type_instance.id)
            session.add(pokemon_type)
    await session.commit()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    pokemon_list = await fetch_pokemon_list()
    print(pokemon_list)
    pokemon_data = await process_pokemon(pokemon_list)
    print(pokemon_data)
    async for session in get_async_session():
        async with session.begin():
            # Insert Pokémon data and related types into the database
            for pkm in pokemon_data:
                pokemon = Pokemon(name=pkm['name'], image_url=pkm['image_url'])
                session.add(pokemon)
                await session.flush()  # Ensure the Pokemon instance gets an ID
                
                for type_name in pkm['types']:
                    # Correctly execute the query and fetch the result
                    stmt = select(Type).where(Type.type_name == type_name)
                    result = await session.execute(stmt)
                    type_instance = result.scalars().first()  # Get the first result
                    
                    if not type_instance:
                        type_instance = Type(type_name=type_name)
                        session.add(type_instance)
                        await session.flush()  # Ensure the Type instance gets an ID
                    
                    pokemon_type = PokemonType(pokemon_id=pokemon.id, type_id=type_instance.id)
                    session.add(pokemon_type)
if __name__ == "__main__":
    asyncio.run(main())