import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "chatbot_logic"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

try:
    from chain import chain
except ImportError as e:
    print(f"Error: No se pudo encontrar chain.py o sus dependencias. {e}")
    chain = None


app = FastAPI(
    title="MiniRodri API",
    description="Servidor de consulta para el proyecto de EDA2",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Consulta(BaseModel):
    pregunta: str

# 4. RUTAS DEL SERVIDOR

@app.get("/")
def home():
    return {
        "mensaje": "Servidor de MiniRodri funcionando",
        "status": "online"
    }

@app.post("/preguntar")
async def responder_pregunta(datos: Consulta):
    """
    Recibe una pregunta y devuelve la respuesta generada por Gemini 1.5 Flash.
    """
    if not chain:
        raise HTTPException(status_code=500, detail="La lógica del chatbot no está cargada.")
    
    if not datos.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        # Ejecución de la cadena RAG
        respuesta = chain.invoke(datos.pregunta)
        return {
            "pregunta": datos.pregunta,
            "respuesta": respuesta
        }
    except Exception as e:
        # Registramos el error en la consola del servidor para debug
        print(f"Error al procesar consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la respuesta.")

# 5. INICIO DEL SERVIDOR
if __name__ == "__main__":
    import uvicorn
    # Se ejecuta en el puerto 8000 por defecto
    uvicorn.run(app, host="0.0.0.0", port=8000)