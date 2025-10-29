# src/routes/sensor.py
from fastapi import APIRouter
from typing import List
from datetime import datetime
from ..models.sensor_data import SensorData, SensorDataCreate
from ..db import fake_sensor_db
from ..services.alert_service import check_sensor_data_for_alerts # 👈 1. Importar

router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensores"]
)

@router.post("/", response_model=SensorData, status_code=201)
async def create_sensor_reading(data: SensorDataCreate):
    """
    Endpoint para que el ESP32 (o el simulador) envíe nuevos datos.
    """
    new_id = len(fake_sensor_db) + 1
    
    new_data = SensorData(
        id=new_id,
        timestamp=datetime.now(),
        **data.dict()
    )
    
    fake_sensor_db.append(new_data)
    print(f"Datos recibidos: {new_data.id}")
    
    # 👈 2. Llamar al servicio de alertas CADA VEZ que llegan datos
    check_sensor_data_for_alerts(new_data)
    
    return new_data

@router.get("/", response_model=List[SensorData])
async def get_all_sensor_readings():
    """
    Endpoint para que el Frontend obtenga los datos.
    """
    return sorted(fake_sensor_db, key=lambda r: r.id, reverse=True)