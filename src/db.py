# src/db.py
from typing import List, Dict, Any
from .models.sensor_data import SensorData
from .models.user_data import User
from datetime import datetime

# --- Base de datos Falsa de Sensores ---
# Es una simple lista que guardará los datos mientras el server corra
fake_sensor_db: List[SensorData] = []

# --- Base de datos Falsa de Usuario (Datos quemados) ---
hardcoded_user = User(
    id=1,
    first_name="Valentina",
    last_name="Mejia Consuegra",
    age=20,
    email="vmejiaconsuegra@gmail.com"
)
fake_alert_db: List[Dict[str, Any]] = []