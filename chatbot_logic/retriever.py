import os
from langchain_core.documents import Document
from typing import List
from vector_store import cargar_almacen_vectorial, crear_almacen_vectorial
from loader import cargar_repositorio_python
from splitter import dividir_codigo

def buscar_fragmentos_relevantes(query: str, k: int = 3, persist_directory: str = "./db") -> List[Document]:
    if persist_directory is None or persist_directory == "./db":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        persist_directory = os.path.join(base_dir, "db")

    if not query or not query.strip():
        print("La consulta no puede estar vacía.")
        return []

    try:
        # Intentar cargar almacén existente
        vector_store = cargar_almacen_vectorial(persist_directory)

        # Si no existe, crearlo desde el repo del backend
        if vector_store is None:
            print("Almacén no encontrado, creando desde el repositorio backend...")
            documentos = cargar_repositorio_python()
            if not documentos:
                print("No se pudieron cargar documentos del repositorio.")
                return []
            fragmentos = dividir_codigo(documentos)
            vector_store = crear_almacen_vectorial(fragmentos, persist_directory)

        if vector_store is None:
            print("No se pudo crear el almacén vectorial.")
            return []

        resultados = vector_store.similarity_search(query, k=k)
        print(f"Se encontraron {len(resultados)} fragmentos relevantes para: '{query}'")
        return resultados

    except Exception as e:
        print("Error durante la búsqueda por similitud:")
        print(e)
        return []