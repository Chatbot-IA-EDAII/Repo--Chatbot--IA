import os
from langchain_core.documents import Document
from typing import List
from loader import cargar_repositorio_python

_documentos_cache = None

# Diccionario de traducciones español → inglés
TRADUCCIONES = {
    "arbol": "tree",
    "arboles": "trees",
    "árbol": "tree",
    "árboles": "trees",
    "busqueda": "search",
    "búsqueda": "search",
    "ordenamiento": "sort",
    "grafo": "graph",
    "grafos": "graphs",
    "cola": "queue",
    "pila": "stack",
    "nodo": "node",
    "recorrido": "traversal",
    "insercion": "insert",
    "inserción": "insert",
    "eliminacion": "delete",
    "eliminación": "delete",
    "binario": "binary",
    "paralelo": "parallel",
    "paralelos": "parallel",
    "archivo": "file",
    "archivos": "files",
}

def buscar_fragmentos_relevantes(query: str, k: int = 5, persist_directory: str = "./db") -> List[Document]:
    global _documentos_cache

    if not query or not query.strip():
        print("La consulta no puede estar vacía.")
        return []

    try:
        if _documentos_cache is None:
            print("Cargando documentos del repositorio backend...")
            _documentos_cache = cargar_repositorio_python()

        if not _documentos_cache:
            print("No se pudieron cargar documentos.")
            return []

        query_lower = query.lower()

        # Generar variaciones de búsqueda
        variaciones = set()
        variaciones.add(query_lower)
        variaciones.add(query_lower.replace(' ', '_'))
        variaciones.add(query_lower.replace(' ', ''))
        variaciones.add(query_lower.replace('_', ' '))

        # Agregar palabras individuales
        palabras = query_lower.replace('_', ' ').split()
        for palabra in palabras:
            variaciones.add(palabra)
            # Traducir al inglés si existe
            if palabra in TRADUCCIONES:
                traduccion = TRADUCCIONES[palabra]
                variaciones.add(traduccion)
                variaciones.add(traduccion + 's')

        print(f"Buscando con variaciones: {variaciones}")

        relevantes = []
        for doc in _documentos_cache:
            contenido = doc.page_content.lower()
            if any(v in contenido for v in variaciones):
                relevantes.append(doc)

        resultado = relevantes[:k] if relevantes else _documentos_cache[:3]
        print(f"Se encontraron {len(resultado)} fragmentos relevantes.")
        return resultado

    except Exception as e:
        print(f"Error durante la búsqueda: {e}")
        return []