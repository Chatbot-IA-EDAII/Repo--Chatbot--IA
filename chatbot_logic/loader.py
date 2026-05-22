import os
import logging
import tempfile
import shutil
import subprocess
from langchain_community.document_loaders import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.document_loaders.parsers.language import Language

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_REPO_URL = "https://github.com/FranciscoCou077/Proyecto-EDAII-Backend.git"

def cargar_repositorio_python(ruta_repo: str = None):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Clonando repositorio backend...")
        subprocess.run(
            ["git", "clone", "--depth=1", "--branch", "dev", BACKEND_REPO_URL, temp_dir],
            check=True,
            capture_output=True
        )
        repo_path = os.path.join(temp_dir, "app", "algoritmos")
        logger.info(f"Cargando algoritmos desde {repo_path}")

        loader = GenericLoader.from_path(
            repo_path,
            glob="**/*.py",
            exclude=[
                "**/.git/**",
                "**/__pycache__/**",
                "**/venv/**",
                "**/env/**",
            ],
            parser=LanguageParser(
                language=Language.PYTHON,
                parser_threshold=500
            )
        )
        documentos = loader.load()
        logger.info(f"Éxito: {len(documentos)} documentos cargados.")
        return documentos

    except Exception as e:
        logger.exception("Error durante la carga del repositorio")
        return []

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)