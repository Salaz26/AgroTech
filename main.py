from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.db import get_sensors, get_user, get_alerts
from src.models.alert import Alert
from src.models.sensor_data import SensorData
from src.models.user_data import User

app = FastAPI()

# Agregar CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/sensors/", response_model=List[SensorData])
def read_sensors():
    return get_sensors()

@app.get("/api/user/", response_model=User)
def read_user():
    return get_user()

@app.get("/api/alerts/", response_model=List[Alert])
def read_alerts():
    return get_alerts()

# Ruta temporal para /api/advice/ (puedes mejorarla después)
@app.get("/api/advice/")
def get_advice():
    return {
        "summary": "El cultivo está en condiciones normales según los sensores actuales",
        "recommendation": "Continuar con el monitoreo regular y verificar niveles de humedad"
    }