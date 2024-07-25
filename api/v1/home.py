from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent.parent / "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {"request": request, "title": "Welcome to Pokémon API!"}
    return templates.TemplateResponse("index.html", context)