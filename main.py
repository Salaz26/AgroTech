from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
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
@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        # Intentar encontrar index.html en varios lugares
        possible_paths = [
            os.path.join(BASE_DIR, "index.html"),
            os.path.join(BASE_DIR, "..", "index.html"),
            "index.html"
        ]
        
        for html_path in possible_paths:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    return f.read()
        
        # Si no encuentra el archivo, retornar página de error informativa
        return f"""
        <html>
            <head><title>AgroTech - Error</title></head>
            <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
                <div style="max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px;">
                    <h1 style="color: #d32f2f;">⚠️ Archivo index.html no encontrado</h1>
                    <p><strong>Directorio base:</strong> {BASE_DIR}</p>
                    <p><strong>Archivos en el directorio:</strong></p>
                    <ul>
                        {"".join([f"<li>{f}</li>" for f in os.listdir(BASE_DIR)])}
                    </ul>
                    <hr>
                    <h2>API Endpoints disponibles:</h2>
                    <ul>
                        <li><a href="/api/sensors/">/api/sensors/</a> - Datos de sensores</li>
                        <li><a href="/api/user/">/api/user/</a> - Información de usuario</li>
                        <li><a href="/api/alerts/">/api/alerts/</a> - Alertas</li>
                        <li><a href="/api/advice/">/api/advice/</a> - Consejos</li>
                    </ul>
                </div>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <head><title>Error</title></head>
            <body style="font-family: Arial; padding: 40px;">
                <h1 style="color: red;">Error al cargar la página</h1>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Directorio:</strong> {BASE_DIR}</p>
            </body>
        </html>
        """

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