# src/routes/ai_advice.py
from fastapi import APIRouter, HTTPException
# 👈 1. Importar el servicio
from ..services.alert_service import get_current_advice 

router = APIRouter(
    prefix="/api/advice",
    tags=["Consejos IA"]
)

@router.get("/")
async def get_ai_advice():
    """
    Obtiene el consejo/resumen actual basado en la última lectura.
    """
    # 👈 2. Pedir el consejo al servicio
    advice = get_current_advice() 
    
    if advice["summary"] == "No hay datos":
        raise HTTPException(status_code=404, detail="No hay datos de sensores todavía.")
    
    # 👈 3. Devolverlo
    return advice