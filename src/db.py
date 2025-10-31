# db.py
from typing import List
from datetime import datetime
from src.models.sensor_data import SensorData
from src.models.user_data import User
from src.models.alert import Alert  # <- ahora import absoluto


# --- Sensores ---
fake_sensor_db: List[SensorData] = [
    SensorData(
        id=1,
        temperature=25,
        humidity=60,
        soil_moisture=40,
        gas_level=1,
        magnetic_field=True,
        uv_level=1,
        timestamp=datetime(2025, 10, 30, 10, 0)
    )
]

# --- Usuario ---
hardcoded_user = User(
    id=1,
    first_name="Valentina",
    last_name="Mejía Consuegra",
    age=20,
    email="vmejiaconsuegra@gmail.com"
)

# --- Alertas ---
fake_alert_db: List[Alert] = [
    Alert(
        id=1,
        level="URGENTE",
        summary="Temperatura alta detectada",
        recommendation="Revisar sistema de enfriamiento inmediatamente",
        timestamp=datetime(2025, 10, 30, 10, 15)
    ),
    Alert(
        id=2,
        level="ALERTA",
        summary="Humedad baja en suelo",
        recommendation="Regar el cultivo en las próximas horas",
        timestamp=datetime(2025, 10, 30, 10, 20)
    ),
    Alert(
        id=3,
        level="PELIGRO",
        summary="Nivel de gas elevado",
        recommendation="Ventilar el área y verificar fugas",
        timestamp=datetime(2025, 10, 30, 11, 30)
    )
]
# --- Funciones de acceso ---
def get_sensors() -> List[SensorData]:
    return fake_sensor_db

def get_user() -> User:
    return hardcoded_user

def get_alerts() -> List[Alert]:
    return fake_alert_db
