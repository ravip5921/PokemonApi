from fastapi import APIRouter
from .pokemon import router as pokemon_router

router = APIRouter()

router.include_router(pokemon_router, prefix="/pokemon", tags=["pokemon"])

# You can include additional routers or middleware specific to v1 here

__all__ = ["api_router"]
