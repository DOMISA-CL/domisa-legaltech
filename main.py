from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any
import datetime

app = FastAPI()

@app.get("/")
def inicio():
    return {"status": "conectado"}

@app.post("/analizar-multas")
async def analizar_multas(datos: Any):
    # Esta versión acepta cualquier formato para evitar el error 422
    try:
        # Simulamos una respuesta de éxito inmediata para probar que el túnel funciona
        return {
            "mensaje": "¡Conexión Exitosa!",
            "ahorro_estimado_clp": 133000,
            "detalle": "IA Domisa operativa"
        }
    except Exception as e:
        return {"error": str(e)}