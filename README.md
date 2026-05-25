# Chatbot IA - EDAII

# 🤖 RAG Chatbot - Análisis de Código Fuente

Repositorio destinado al desarrollo de un sistema de **Generación Aumentada por Recuperación (RAG)** diseñado para interpretar y analizar código fuente de repositorios GitHub, enfocado en algoritmos y estructuras de datos.

## 🚀 Hoja de Ruta Técnica

El proyecto está dividido en módulos fundamentales para el backend, el procesamiento de datos y el despliegue del servicio:

### Lógica Principal (Motor RAG)
1. `loader.py`: Carga y filtrado de scripts de Python, ignorando archivos basura.
2. `splitter.py`: División de código manteniendo la estructura lógica de clases y funciones.
3. `embeddings.py`: Generación de representaciones vectoriales del código.
4. `vector_store.py`: Almacenamiento persistente en base de datos vectorial (ChromaDB).
5. `retriever.py`: Motor de búsqueda para extraer los fragmentos de código más relevantes.
6. `prompt_template.py`: Ingeniería de prompts para asegurar respuestas técnicas precisas.
7. `chain.py`: Orquestación de la lógica del chatbot usando LangChain (LCEL).
8. `main.py`: Interfaz de usuario final y bucle de ejecución del chat en consola.

### Arquitectura de Datos e Integración (Pipeline y API)
9. **`utils/data_handler.py`**: Pipeline de procesamiento estructurado basado en POO. Extrae metadatos, descripciones (docstrings) y código puro mediante AST, exportando una base de conocimiento en formato JSON.
10. **`setup_env.py`**: Script de automatización para la instalación de dependencias y configuración segura del entorno local.
11. **`server.py`**: API REST construida con **FastAPI** para exponer el motor RAG y permitir la comunicación directa con interfaces gráficas (UI) de otros equipos.

### Variables de entorno
Antes de ejecutar el chatbot, copia [`.env.example`](.env.example) a `.env` y agrega tu `GOOGLE_API_KEY`. No dejes claves reales hardcodeadas en `chain.py`.

## Integrantes 
- Jim Nava Bryan
- Martínez Mondragón Benjamín
- Arroyo Castañon Dulce Carolina
- Perea Yañez Oscar
- Hernandez Camargo Josue
- Galindo Contreras Angel Gabriel
- Marín Pérez Daniela
- Escobedo Reyes Emma Esmeralda
- Martínez García Nour
- Jiménez Vega José Enrique
- Orozco González Samuel Alejandro
- Zambrano Mota María Fernanda

## 📂 Estructura del Repositorio

```text
/
├── chatbot_logic/         # Scripts principales del motor RAG (Módulos 1-8)
├── data/                  # Directorio autogenerado para almacenar los JSON procesados
├── repositorios_fuente/   # Códigos fuente crudos (.py) que serán analizados
├── utils/                 # Herramientas de preprocesamiento (data_handler.py)
├── .env.example           # Plantilla segura de variables de entorno y API Keys
├── .gitignore             # Reglas de exclusión para seguridad de credenciales
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias (LangChain, FastAPI, ChromaDB, etc.)
├── server.py              # Punto de entrada de la API REST
└── setup_env.py           # Script automatizado para preparar el entorno