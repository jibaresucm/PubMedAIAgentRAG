# PubMed AI Agent: Sistema de Razonamiento Médico y Recuperación Semántica (RAG)

Agente de IA RAG con herramientas para descargar abstracts directamente desde pubmed y herramientas para acceder a esos documentos.

Utiliza una base de datos vectorial para realizar una busqueda semántica y hacer el retrieve de datos relacionados con la query del usuario.

Manejo del contexto implementado desde 0.

# Como usarlo
Necesitas instalar todas las dependencias como llama_cpp(compilado si tienes una gráfica), customtkinter, huggingface_hub, chroma_db, biopython...

Deberás descargar un modelo de lenguaje y otro de embeddings con la herramienta que se encuentra en model_downloads, yo descargué Gemma 4 para el LLM.
Tienes que guardar los .gguf o el formato de modelo compatible con llama_cpp en las carpetas de modelos/llm o modelos/embedding respectivamente y cambiar el nombre del archivo en el settings.py.
