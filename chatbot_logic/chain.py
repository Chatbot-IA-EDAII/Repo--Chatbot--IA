import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

from prompt_template import prompt_template
from retriever import buscar_fragmentos_relevantes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError("Falta GROQ_API_KEY.")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    api_key=groq_api_key
)

def format_docs(docs):
    if not docs:
        return "No se encontró información en la base de datos para esta consulta."
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

chain = (
    {
        "context": RunnableLambda(lambda x: buscar_fragmentos_relevantes(x)) | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt_template
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    pregunta = "¿Qué operaciones puede realizar la clase Calculadora que está en el código?"
    print(f"\n--- CONSULTANDO A MiniRodri ---")
    try:
        respuesta = chain.invoke(pregunta)
        print(f"\nRespuesta:\n{respuesta}")
    except Exception as e:
        print(f"\nError en la comunicación: {e}")