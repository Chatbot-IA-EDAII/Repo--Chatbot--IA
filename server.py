import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "chatbot_logic"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    try:
        from chain import chain as rag_chain
        chain = rag_chain
        print("✅ RAG inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar RAG: {e}")
    yield

app = FastAPI(
    title="MiniRodri API",
    description="Servidor de consulta para el proyecto de EDA2",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Consulta(BaseModel):
    pregunta: str

@app.get("/")
def home():
    return {
        "mensaje": "Servidor de MiniRodri funcionando",
        "status": "online"
    }

@app.post("/preguntar")
async def responder_pregunta(datos: Consulta):
    if not chain:
        raise HTTPException(status_code=500, detail="La lógica del chatbot no está cargada.")
    
    if not datos.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        respuesta = chain.invoke(datos.pregunta)
        return {
            "pregunta": datos.pregunta,
            "respuesta": respuesta
        }
    except Exception as e:
        print(f"Error al procesar consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la respuesta.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)