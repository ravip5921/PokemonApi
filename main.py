from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1 import pokemon,home
from database import Base, engine
from dotenv import load_dotenv
import os
import asyncio
import uvicorn

dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path)

app = FastAPI()

# static files [JS and CSS]
app.mount("/static", StaticFiles(directory="static"), name="static")

loop = asyncio.get_event_loop()

# Include routers
app.include_router(pokemon.router, prefix="/api/v1")
app.include_router(home.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True, loop=loop)