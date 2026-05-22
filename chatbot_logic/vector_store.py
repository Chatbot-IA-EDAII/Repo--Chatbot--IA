import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Optional
from embeddings import crear_modelo_embeddings
from splitter import dividir_codigo
 
 

DIRECTORIO_DB = "./db"
 
 
def crear_almacen_vectorial(
    documentos: List[Document],
    persist_directory: str = DIRECTORIO_DB
) -> Optional[Chroma]:
    """
    Crea un almacén vectorial ChromaDB a partir de una lista de documentos,
    genera sus embeddings y los persiste en disco.
 
    Parámetros:
        documentos (List[Document]):
            Lista de fragmentos de código generados por splitter.py (Tarea 2).
 
        persist_directory (str):
            Ruta de la carpeta donde se guardará la base de datos vectorial.
            Por defecto: "./db"
 
    Retorna:
        Chroma:
            Instancia del almacén vectorial listo para hacer búsquedas.
        None:
            Si ocurre algún error durante la creación.
    """
 
    if not documentos:
        print("No se recibieron documentos para crear el almacén vectorial.")
        return None
 
    try:
 
        print(f"Inicializando modelo de embeddings...")
        modelo_embeddings = crear_modelo_embeddings()
 
        print(f"Creando almacén vectorial con {len(documentos)} fragmentos...")
        vector_store = Chroma.from_documents(
            documents=documentos,
            embedding=modelo_embeddings,
            persist_directory=persist_directory
        )
 
        print(f"Almacén vectorial creado y persistido en: '{persist_directory}'")
        return vector_store
 
    except Exception as e:
        print("Error al crear el almacén vectorial:")
        print(e)
        return None
 
 
def cargar_almacen_vectorial(
    persist_directory: str = DIRECTORIO_DB
) -> Optional[Chroma]:
    """
    Carga un almacén vectorial ChromaDB ya existente desde disco,
    evitando recalcular los embeddings.
 
    Parámetros:
        persist_directory (str):
            Ruta de la carpeta donde está guardada la base de datos vectorial.
            Por defecto: "./db"
 
    Retorna:
        Chroma:
            Instancia del almacén vectorial listo para hacer búsquedas.
        None:
            Si ocurre algún error durante la carga.
    """
 
    try:
 
        print(f"Cargando almacén vectorial desde: '{persist_directory}'...")
        modelo_embeddings = crear_modelo_embeddings()
 
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=modelo_embeddings
        )
 
        print("Almacén vectorial cargado exitosamente.")
        return vector_store
 
    except Exception as e:
        print("Error al cargar el almacén vectorial:")
        print(e)
        return None
 
 
# ======================================
# PRUEBA LOCAL
# ======================================
 
if __name__ == "__main__":
 
    codigo_ejemplo = """
def suma(a, b):
    return a + b
 
def resta(a, b):
    return a - b
 
class Calculadora:
 
    def multiplicar(self, a, b):
        return a * b
 
    def dividir(self, a, b):
        if b == 0:
            return "Error: división entre cero"
        return a / b
"""
 
    documento_prueba = Document(page_content=codigo_ejemplo)
 
    print("===== PASO 1: Fragmentando código =====")
    fragmentos = dividir_codigo([documento_prueba])
 
    print("\n===== PASO 2: Creando almacén vectorial =====")
    vector_store = crear_almacen_vectorial(fragmentos)
 
    if vector_store is None:
        print("No se pudo crear el almacén vectorial.")
        exit(1)
 
    print("\n===== PASO 3: Cargando almacén desde disco =====")
    vector_store_cargado = cargar_almacen_vectorial()
 
    if vector_store_cargado:
        resultados = vector_store_cargado.similarity_search("función suma", k=2)
 
        print(f"\n===== BÚSQUEDA DE PRUEBA =====")
        print(f"Fragmentos encontrados: {len(resultados)}\n")
 
        for i, doc in enumerate(resultados, start=1):
            print(f"--- Resultado {i} ---")
            print(doc.page_content)
            print()