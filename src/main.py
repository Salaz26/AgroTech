# src/main.py
import os # Para manejar rutas de archivos
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # Para servir el frontend
from fastapi.responses import FileResponse # Para servir el index.html
from fastapi.middleware.cors import CORSMiddleware # Para permitir la conexión

# Importamos nuestros routers
# 👇 ¡Asegúrate de importar el nuevo router de 'alerts'!
from .routes import sensor, user, ai_advice, alerts

# --- Configuración de Rutas Absolutas ---
# Esto evita el error "Directory does not exist"
# BASE_DIR apunta a la carpeta 'src' donde está este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_DIR apunta a 'src/static'
STATIC_DIR = os.path.join(BASE_DIR, "static")


# --- Creación de la App ---
app = FastAPI(title="AgroTech API")


# --- Configurar CORS ---
# Esto permite que tu frontend (en localhost) se comunique con tu backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todos los orígenes (simple para dev)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos los headers
)


# --- Incluir Rutas de la API ---
# Aquí conectamos los archivos de la carpeta 'routes'
app.include_router(sensor.router)
app.include_router(user.router)
app.include_router(ai_advice.router)
app.include_router(alerts.router) # 👈 Esta es la línea que agregamos


# --- Servir el Frontend ---

# 1. Monta la carpeta 'static' usando la ruta absoluta
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# 2. Sirve el 'index.html' como la página principal (ruta "/")
@app.get("/")
async def read_index():
    # Devuelve el archivo index.html usando la ruta absoluta
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))