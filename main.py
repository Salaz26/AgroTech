from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import sys, os

# Asegura que la carpeta src esté en el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

# Importar desde src/
from db import get_sensors, get_user, get_alerts
from models.alert import Alert
from models.sensor_data import SensorData
from models.user_data import User

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para servir el HTML principal
@app.get("/")
def read_root():
    html_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(html_path)

@app.get("/api/sensors/", response_model=List[SensorData])
def read_sensors():
    return get_sensors()

@app.get("/api/user/", response_model=User)
def read_user():
    return get_user()

@app.get("/api/alerts/", response_model=List[Alert])
def read_alerts():
    return get_alerts()

@app.get("/api/advice/")
def get_advice():
    return {
        "summary": "El cultivo está en condiciones normales según los sensores actuales",
        "recommendation": "Continuar con el monitoreo regular y verificar niveles de humedad"
    }