# src/models/sensor_data.py
from pydantic import BaseModel
from datetime import datetime

# Modelo para los datos que LLEGAN desde el ESP32
class SensorDataCreate(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: int
    gas_level: int
    magnetic_field: bool
    uv_level: int

# Modelo para los datos como se GUARDAN en la DB (con ID y timestamp)
class SensorData(SensorDataCreate):
    id: int
    timestamp: datetime