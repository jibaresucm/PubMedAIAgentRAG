import chromadb
from settings import config

client = chromadb.PersistentClient(path = config.VECTOR_DB_PATH)

collection = client.get_or_create_collection(
    name=config.PUBMED_DOCS_COLLECTION,
    metadata={"hnsw:space": "cosine"} 
)

print("Colección creada")