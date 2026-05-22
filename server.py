import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "chatbot_logic"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

chain = None

def get_chain():
    global chain
    if chain is None:
        try:
            from chain import chain as rag_chain
            chain = rag_chain
            print("✅ RAG inicializado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar RAG: {e}")
            raise
    return chain

app = FastAPI(
    title="MiniRodri API",
    description="Servidor de consulta para el proyecto de EDA2",
    version="1.0.0"
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
    if not datos.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        rag = get_chain()
        respuesta = rag.invoke(datos.pregunta)
        return {
            "pregunta": datos.pregunta,
            "respuesta": respuesta
        }
    except Exception as e:
        print(f"Error al procesar consulta: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)