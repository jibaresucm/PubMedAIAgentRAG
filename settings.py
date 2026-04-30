import os

class Settings:
    #Carpetas y paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")
    MODELS_PATH = os.path.join(BASE_DIR, "modelos")
    EMBEDDING_MODELS_PATH = os.path.join(MODELS_PATH, "embedding")
    LLM_MODELS_PATH = os.path.join(MODELS_PATH, "llm")

    #Para pubmed
    EMAIL = "ejemploemail@gmail.com"
    MAX_DOCUMENTS = 15
    
    #Modelos elegidos
    EMBEDDING_MODEL = "v5-small-retrieval-IQ4_NL.gguf"
    LLM_MODEL = "gemma-4-E4B-it-IQ4_NL.gguf"
    EMBEDDING_CONTEXT = 2048
    LLM_CONTEXT = 65536
    
    #Vector db
    PUBMED_DOCS_COLLECTION = "pubmed_documents"


config = Settings()

for path in [config.VECTOR_DB_PATH]:
    if not os.path.exists(path):
        print("Creating path...")
        os.makedirs(path)