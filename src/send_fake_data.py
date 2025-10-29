# src/send_fake_data.py
import requests
import time
import random

# La URL de tu API
API_URL = "http://127.0.0.1:8000/api/sensors/"

# --- Definimos los escenarios de prueba ---
# Estos datos están diseñados para activar tu "IA"
escenarios = [
    {
        "nombre": "CONDICIÓN NORMAL",
        "datos": {
            "temperature": 24.5,
            "humidity": 65.0,
            "soil_moisture": 2200, 
            "gas_level": 350,
            "magnetic_field": False,
            "uv_level": 750
        }
    },
    {
        "nombre": "ALERTA: SUELO MUY SECO",
        "datos": {
            "temperature": 28.0,
            "humidity": 50.0,
            "soil_moisture": 3500, 
            "gas_level": 400,
            "magnetic_field": False,
            "uv_level": 900
        }
    },
    
    # --- 👇 NUEVO ESCENARIO POSITIVO ---
    {
        "nombre": "☀️ CONDICIÓN ÓPTIMA (MAÑANA)", 
        "datos": {
            "temperature": 22.5,
            "humidity": 75.0,
            "soil_moisture": 2300, # Húmedo pero no ahogado
            "gas_level": 300,      # Limpio
            "magnetic_field": False,
            "uv_level": 400        # UV bajo
        }
    },
    # --- FIN NUEVO ESCENARIO ---
    
    {
        "nombre": "ALERTA: TEMPERATURA ALTA",
        "datos": {
            "temperature": 39.5,
            "humidity": 45.0,
            "soil_moisture": 2500,
            "gas_level": 500,
            "magnetic_field": False,
            "uv_level": 1200
        }
    },
    {
        "nombre": "ALERTA: SUELO MUY HÚMEDO",
        "datos": {
            "temperature": 22.0,
            "humidity": 85.0,
            "soil_moisture": 1200,
            "gas_level": 320,
            "magnetic_field": False,
            "uv_level": 300
        }
    },
    
    # --- 👇 NUEVO ESCENARIO POSITIVO ---
    {
        "nombre": "🌱 CONDICIÓN ÓPTIMA (TARDE)",
        "datos": {
            "temperature": 26.0,
            "humidity": 68.0,
            "soil_moisture": 2100, # Perfecto
            "gas_level": 320,
            "magnetic_field": False,
            "uv_level": 800        # UV moderado
        }
    },
    # --- FIN NUEVO ESCENARIO ---
    
    {
        "nombre": "ALERTA: DETECCIÓN DE GAS",
        "datos": {
            "temperature": 25.0,
            "humidity": 60.0,
            "soil_moisture": 2300,
            "gas_level": 2100, 
            "magnetic_field": True,
            "uv_level": 800
        }
    }
]

def enviar_datos_falsos():
    print("--- Iniciando Simulador ESP32 ---")
    print(f"Enviando datos a: {API_URL}")
    
    i = 0
    while True:
        # Elegimos un escenario de la lista
        escenario = escenarios[i % len(escenarios)]
        
        print("\n---------------------------------")
        print(f"Enviando escenario: {escenario['nombre']}")
        
        # Tomamos los datos base del escenario
        payload = escenario['datos'].copy()
        
        # Añadimos un poco de "ruido" aleatorio para que no sea idéntico
        payload['temperature'] += random.uniform(-0.5, 0.5)
        payload['humidity'] += random.uniform(-2.0, 2.0)
        
        try:
            # Enviamos la petición POST
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 201:
                print(f"✅ Éxito: Datos enviados. Respuesta: {response.json()['id']}")
            else:
                print(f"❌ Error: El servidor respondió [ {response.status_code} ]")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor.")
            print("Asegúrate de que el servidor 'uvicorn' esté corriendo.")
        
        # Aumentamos el contador y esperamos 15 segundos
        i += 1
        print("---------------------------------")
        print("Durmiendo 15 segundos...")
        time.sleep(15)

if __name__ == "__main__":
    enviar_datos_falsos()