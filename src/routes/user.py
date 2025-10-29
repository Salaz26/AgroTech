# src/routes/user.py
from fastapi import APIRouter
# Importamos el modelo y el usuario quemado
from ..models.user_data import User
from ..db import hardcoded_user

router = APIRouter(
    prefix="/api/user",
    tags=["Usuario"]
)

@router.get("/", response_model=User)
async def get_user_info():
    """
    Devuelve la información del usuario único (quemado).
    """
    return hardcoded_user