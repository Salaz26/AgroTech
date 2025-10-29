# src/services/alert_service.py
from ..db import fake_alert_db, fake_sensor_db
from ..models.sensor_data import SensorData
from datetime import datetime

def log_alert(level: str, summary: str, recommendation: str):
    """
    Guarda una alerta en la DB, evitando duplicados
    (no guarda la misma alerta dos veces seguidas).
    """
    if fake_alert_db and fake_alert_db[-1]["summary"] == summary:
        return  # Evita duplicados
    
    new_alert = {
        "id": len(fake_alert_db) + 1,
        "timestamp": datetime.now(),
        "level": level,
        "summary": summary,
        "recommendation": recommendation
    }
    fake_alert_db.append(new_alert)
    print(f"🚨 ALERTA GENERADA: {level} - {summary}")

def check_sensor_data_for_alerts(data: SensorData):
    """
    Revisa los datos de un sensor y LOGUEA alertas si es necesario.
    Esta función se llama CADA VEZ que llegan datos nuevos.
    """
    # Chequeamos todas las condiciones
    # (¡Recuerda calibrar estos valores!)
    if data.soil_moisture > 3000:
        log_alert("URGENTE", "El suelo está extremadamente seco.", "¡Acción Urgente! Se necesita riego inmediato.")
    
    elif data.soil_moisture < 1500:
        log_alert("ALERTA", "El suelo está muy húmedo (ahogado).", "Detener el riego. Revisar el drenaje del cultivo.")

    if data.temperature > 38.0:
        log_alert("ALERTA", "La temperatura es peligrosamente alta.", "Activar ventilación o sombreado.")
        
    if data.gas_level > 2000:
        log_alert("PELIGRO", "Nivel de gas (CO/LPG) detectado.", "Revisar el área por posibles fugas o mala ventilación.")

def get_current_advice():
    """
    Obtiene el consejo actual para la Pestaña 2 (Resumen IA).
    Revisa el último dato y da un consejo en tiempo real.
    """
    if not fake_sensor_db:
        return {"summary": "No hay datos", "recommendation": "Esperando datos del sensor..."}

    latest_data = fake_sensor_db[-1]
    
    # --- 1. CHEQUEO DE ALERTAS (Prioridad alta) ---
    if latest_data.soil_moisture > 3000:
        return {"summary": "El suelo está extremadamente seco.", "recommendation": "¡Acción Urgente! Se necesita riego inmediato."}
    if latest_data.soil_moisture < 1500:
        return {"summary": "El suelo está muy húmedo (ahogado).", "recommendation": "Detener el riego. Revisar el drenaje del cultivo."}
    if latest_data.temperature > 38.0:
        return {"summary": "La temperatura es peligrosamente alta.", "recommendation": "Activar ventilación o sombreado."}
    if latest_data.gas_level > 2000:
        return {"summary": "Nivel de gas (CO/LPG) detectado.", "recommendation": "Revisar el área por posibles fugas o mala ventilación."}

    # --- 2. 👇 CHEQUEO POSITIVO ---
    # Si no hay alertas, buscamos el "punto dulce" (sweet spot).
    # (Ajusta estos rangos según tu cultivo)
    is_good_soil = 1800 < latest_data.soil_moisture < 2800
    is_good_temp = 20 < latest_data.temperature < 30
    
    if is_good_soil and is_good_temp:
        summary = "¡Condiciones Óptimas! 🌱"
        recommendation = "El cultivo está en su punto ideal de humedad y temperatura. No se requiere ninguna acción."
        return {"summary": summary, "recommendation": recommendation}

    # --- 3. MENSAJE "NORMAL" (Si no es alerta ni óptimo) ---
    summary = f"Lectura normal: {latest_data.temperature:.1f}°C y {latest_data.humidity:.1f}% de humedad."
    recommendation = "Todo parece estar en orden, pero monitoreando condiciones."
    return {"summary": summary, "recommendation": recommendation}

#
# --- LA FUNCIÓN DUPLICADA QUE ESTABA AQUÍ FUE ELIMINADA ---
#