import os
from langchain_core.documents import Document
from typing import List
from loader import cargar_repositorio_python

_documentos_cache = None

def buscar_fragmentos_relevantes(query: str, k: int = 5, persist_directory: str = "./db") -> List[Document]:
    global _documentos_cache

    if not query or not query.strip():
        print("La consulta no puede estar vacía.")
        return []

    try:
        # Usar cache para no clonar el repo en cada petición
        if _documentos_cache is None:
            print("Cargando documentos del repositorio backend...")
            _documentos_cache = cargar_repositorio_python()

        if not _documentos_cache:
            print("No se pudieron cargar documentos.")
            return []

        # Búsqueda simple por palabras clave en vez de vectores
        query_lower = query.lower()
        relevantes = []

        for doc in _documentos_cache:
            contenido = doc.page_content.lower()
            palabras = query_lower.split()
            if any(palabra in contenido for palabra in palabras):
                relevantes.append(doc)

        # Retornar los k más relevantes
        resultado = relevantes[:k] if relevantes else _documentos_cache[:k]
        print(f"Se encontraron {len(resultado)} fragmentos relevantes.")
        return resultado

    except Exception as e:
        print(f"Error durante la búsqueda: {e}")
        return []