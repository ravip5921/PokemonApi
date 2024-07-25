
import os
import configparser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

# Load environment variables from .env file
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

config = configparser.ConfigParser()
config.read('config/config.ini')

database_url = os.getenv('DATABASE_URL') or config['database']['url']

# Create async engine
engine = create_async_engine(database_url, echo=True)

# Create AsyncSession class for use in async contexts
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for declarative class definitions
Base = declarative_base()

# Function to get an async session
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session