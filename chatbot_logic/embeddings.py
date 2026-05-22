from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
import os

def crear_modelo_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

def generar_embeddings(textos: List[str]) -> List[List[float]]:
    if not textos:
        return []

    try:
        modelo = crear_modelo_embeddings()
        vectores = modelo.embed_documents(textos)
        print(f"Se generaron {len(vectores)} embeddings.")
        return vectores

    except Exception as e:
        print("Error al generar embeddings:")
        print(e)
        return []

if __name__ == "__main__":
    textos_prueba = [
        "def suma(a, b): return a + b",
        "def resta(a, b): return a - b"
    ]

    embeddings = generar_embeddings(textos_prueba)
    print("Cantidad de vectores:", len(embeddings))

    if embeddings:
        print("Dimensión del primer vector:", len(embeddings[0]))