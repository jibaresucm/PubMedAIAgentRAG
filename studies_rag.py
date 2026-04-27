import json

import chromadb
from settings import config
from create_models import get_embedding_model

def get_documents(query, n_docs):
    client = chromadb.PersistentClient(path = config.VECTOR_DB_PATH)
    collection = client.get_collection(name= config.PUBMED_DOCS_COLLECTION)
    
    emb_model = get_embedding_model()
    output = emb_model.create_embedding(input=query)
    vector = output['data'][0]['embedding']
    
    results = collection.query(
        query_embeddings=[vector],
        n_results=n_docs,
        include=["documents"]
    )
    
    ids = results['ids'][0]
    docs = results['documents'][0]
    
    ret = dict(list(zip(ids, docs)))
    
    return ret

def studies_rag(params):
    query = params["query"]
    max_results = params["max_results"]

    ret = get_documents(query, max_results)
    
    return "studies_rag" + json.dumps(ret, indent=4, ensure_ascii=False)
