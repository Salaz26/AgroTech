# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

# Importa tu app principal y las bases de datos falsas
from src.main import app
from src.db import fake_sensor_db, fake_alert_db

@pytest.fixture(scope="module")
def client():
    """
    Crea un cliente de pruebas para llamar a la API.
    Se crea una vez por módulo (todos los tests usan el mismo cliente).
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def reset_dbs_before_each_test():
    """
    Limpia las bases de datos en memoria ANTES de cada prueba.
    'autouse=True' hace que se ejecute automáticamente.
    """
    fake_sensor_db.clear()
    fake_alert_db.clear()
    yield # Aquí es donde la prueba se ejecuta
    
    # Opcional: puedes limpiar también después
    # fake_sensor_db.clear()
    # fake_alert_db.clear()