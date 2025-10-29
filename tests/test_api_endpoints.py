# tests/test_api_endpoints.py
from src.db import fake_sensor_db, fake_alert_db

# --- Datos de prueba ---
# Los mismos que tu simulador para consistencia
DATA_NORMAL = {
    "temperature": 25.0, "humidity": 60.0, "soil_moisture": 2200,
    "gas_level": 350, "magnetic_field": False, "uv_level": 750
}
DATA_SECO = {
    "temperature": 30.0, "humidity": 50.0, "soil_moisture": 3500, # Alerta
    "gas_level": 400, "magnetic_field": False, "uv_level": 900
}
DATA_OPTIMO = {
    "temperature": 23.0, "humidity": 70.0, "soil_moisture": 2300, # Óptimo
    "gas_level": 300, "magnetic_field": False, "uv_level": 400
}

# tests/test_api_endpoints.py

# --- Datos para las nuevas pruebas (puedes ponerlos arriba) ---
DATA_HUMEDO = {
    "temperature": 20.0, "humidity": 90.0, "soil_moisture": 1200, # Alerta
    "gas_level": 300, "magnetic_field": False, "uv_level": 200
}
DATA_CALIENTE = {
    "temperature": 40.0, "humidity": 30.0, "soil_moisture": 2500, # Alerta
    "gas_level": 300, "magnetic_field": False, "uv_level": 1500
}
DATA_GAS = {
    "temperature": 25.0, "humidity": 60.0, "soil_moisture": 2200,
    "gas_level": 3000, "magnetic_field": False, "uv_level": 750 # Alerta
}

# --- 👇 AÑADE ESTAS NUEVAS PRUEBAS ---

def test_alert_for_soil_humid(client):
    """
    Prueba que se genere una alerta de "Suelo Húmedo".
    """
    client.post("/api/sensors/", json=DATA_HUMEDO)
    
    assert len(fake_alert_db) == 1
    assert fake_alert_db[0]["level"] == "ALERTA"
    assert "muy húmedo" in fake_alert_db[0]["summary"]

def test_alert_for_high_temp(client):
    """
    Prueba que se genere una alerta de "Temperatura Alta".
    """
    client.post("/api/sensors/", json=DATA_CALIENTE)
    
    assert len(fake_alert_db) == 1
    assert fake_alert_db[0]["level"] == "ALERTA"
    assert "temperatura" in fake_alert_db[0]["summary"]

def test_alert_for_gas_level(client):
    """
    Prueba que se genere una alerta de "Detección de Gas".
    """
    client.post("/api/sensors/", json=DATA_GAS)
    
    assert len(fake_alert_db) == 1
    assert fake_alert_db[0]["level"] == "PELIGRO"
    assert "Nivel de gas" in fake_alert_db[0]["summary"]

def test_advice_for_high_temp(client):
    """
    Prueba que el Resumen IA reporte la temperatura alta.
    """
    client.post("/api/sensors/", json=DATA_CALIENTE)
    
    response = client.get("/api/advice/")
    assert response.status_code == 200
    assert "temperatura" in response.json()["summary"]

def test_read_root(client):
    """Prueba que la ruta principal (/) cargue el index.html."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

# tests/test_api_endpoints.py
...
def test_get_user(client):
    """Prueba el endpoint de usuario (datos quemados)."""
    response = client.get("/api/user/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    # 👇 ESTA LÍNEA ESTÁ MAL
    # assert data["email"] == "usuario@ejemplo.com" 
    
    # 👇 ARREGLA PONIENDO EL EMAIL REAL DE TUS DATOS QUEMADOS
    assert data["email"] == "vmejiaconsuegra@gmail.com"

def test_get_empty_sensors(client):
    """Prueba que /api/sensors/ devuelva [] si está vacío."""
    response = client.get("/api/sensors/")
    assert response.status_code == 200
    assert response.json() == []

def test_post_sensor_data_normal(client):
    """
    Prueba que enviar datos normales:
    1. Responda 201 (Created).
    2. Guarde 1 dato en fake_sensor_db.
    3. NO guarde ninguna alerta en fake_alert_db.
    """
    response = client.post("/api/sensors/", json=DATA_NORMAL)
    
    # 1. Revisa la respuesta
    assert response.status_code == 201
    assert response.json()["temperature"] == DATA_NORMAL["temperature"]
    
    # 2. Revisa la base de datos de sensores
    assert len(fake_sensor_db) == 1
    assert fake_sensor_db[0].soil_moisture == DATA_NORMAL["soil_moisture"]
    
    # 3. Revisa la base de datos de alertas
    assert len(fake_alert_db) == 0

def test_post_sensor_data_triggers_alert(client):
    """
    Prueba que enviar datos de ALERTA:
    1. Responda 201 (Created).
    2. Guarde 1 dato en fake_sensor_db.
    3. SÍ guarde 1 alerta en fake_alert_db.
    """
    response = client.post("/api/sensors/", json=DATA_SECO)
    
    # 1. Revisa la respuesta
    assert response.status_code == 201
    
    # 2. Revisa la base de datos de sensores
    assert len(fake_sensor_db) == 1
    
    # 3. Revisa la base de datos de alertas
    assert len(fake_alert_db) == 1
    assert fake_alert_db[0]["level"] == "URGENTE"
    assert fake_alert_db[0]["summary"] == "El suelo está extremadamente seco."

def test_get_alert_log(client):
    """Prueba el log de alertas después de crear una."""
    # Primero, creamos una alerta
    client.post("/api/sensors/", json=DATA_SECO)
    
    # Ahora, pedimos el log
    response = client.get("/api/alerts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["summary"] == "El suelo está extremadamente seco."

def test_get_advice_no_data(client):
    """Prueba que el resumen IA dé un error 404 si no hay datos."""
    response = client.get("/api/advice/")
    assert response.status_code == 404
    assert response.json()["detail"] == "No hay datos de sensores todavía."

def test_get_advice_optimal(client):
    """Prueba que el resumen IA reconozca condiciones óptimas."""
    # Primero, enviamos datos óptimos
    client.post("/api/sensors/", json=DATA_OPTIMO)
    
    # Pedimos el consejo
    response = client.get("/api/advice/")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "¡Condiciones Óptimas! 🌱"
    assert data["recommendation"] == "El cultivo está en su punto ideal de humedad y temperatura. No se requiere ninguna acción."

def test_post_sensor_data_missing_field(client):
    """
    Prueba de validación (¡clave para cobertura!).
    Envía datos incompletos (falta 'uv_level') y espera un error 422.
    """
    data_incompleta = DATA_NORMAL.copy()
    del data_incompleta["uv_level"] # Quitamos un campo requerido
    
    response = client.post("/api/sensors/", json=data_incompleta)
    
    # 422 = Unprocessable Entity (Error de validación)
    assert response.status_code == 422 
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", "uv_level"]
    
    # ... (deja todas tus otras pruebas y datos de prueba como están) ...

def test_get_advice_normal(client):
    """
    Prueba que el resumen IA devuelva el mensaje "normal"
    cuando no hay ni alertas ni condiciones óptimas.
    
    ESTA PRUEBA CUBRE LAS LÍNEAS DEL "CASO NORMAL" EN get_current_advice()
    """
    # DATA_NORMAL no cumple ni las alertas ni las condiciones óptimas (1800-2800)
    data_normal_fuera_de_rango = {
        "temperature": 25.0, "humidity": 60.0, "soil_moisture": 2900, # Ni alerta, ni óptimo
        "gas_level": 350, "magnetic_field": False, "uv_level": 750
    }
    
    client.post("/api/sensors/", json=data_normal_fuera_de_rango)
    
    response = client.get("/api/advice/")
    assert response.status_code == 200
    data = response.json()
    assert "Lectura normal" in data["summary"]
    assert "Todo parece estar en orden" in data["recommendation"]

def test_log_alert_avoids_duplicates(client):
    """
    Prueba que la función log_alert no guarde duplicados.
    
    ESTA PRUEBA CUBRE LAS LÍNEAS "return # Evita duplicados" EN log_alert()
    """
    # Enviamos datos de suelo seco
    client.post("/api/sensors/", json=DATA_SECO)
    # Verificamos que se guardó 1 alerta
    assert len(fake_alert_db) == 1
    
    # Volvemos a enviar EXACTAMENTE los mismos datos
    client.post("/api/sensors/", json=DATA_SECO)
    
    # Verificamos que el contador NO aumentó.
    # La lógica de "evitar duplicados" funcionó.
    assert len(fake_alert_db) == 1