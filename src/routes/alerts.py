# src/routes/alerts.py
from fastapi import APIRouter
from typing import List, Dict, Any
from ..db import fake_alert_db # Importar la DB de alertas

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alertas"]
)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_alert_log():
    """
    Devuelve el registro histórico de todas las alertas generadas.
    """
    # Devolver en orden inverso (la más nueva primero)
    return sorted(fake_alert_db, key=lambda a: a["id"], reverse=True)