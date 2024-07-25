from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_url = Column(String)

    types = relationship('Type', secondary='pokemon_type')

class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type_name = Column(String)

class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'), primary_key=True)