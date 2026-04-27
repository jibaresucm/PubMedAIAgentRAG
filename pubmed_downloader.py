from settings import config
import time
from Bio import Entrez
import chromadb
from create_models import get_embedding_model

def index_documents_to_db(document_list, collection):
    """
    Recibe lista de tuplas (id_documento(String), texto (String)) para document_list
    Collection es un chromadb collection
    """
    total = len(document_list)
    
    print(f"Indexando {total} documentos...")
    
    emb = get_embedding_model()
    
    counter = 0
    for doc_id, text in document_list:
        
            emb_vector = emb.create_embedding(text)['data'][0]['embedding']
            
            collection.add(
                ids = [doc_id],
                embeddings = [emb_vector],
                documents = [text],
            )
            
            counter +=1
            print(f"Indexado {counter}/{total}")
        

def download_studies(text_query, max_docs = config.MAX_DOCUMENTS, existing_ids = []):
    
    """
    Descarga documentos de pubmed i los devuelve en una lista de tuplas  (id_documento(String), texto (String))
    """
    
    print("Searching documents in PubMed...")
    
    if(max_docs > config.MAX_DOCUMENTS): max_docs = config.MAX_DOCUMENTS
    
    document_list = []
    
    eids_set = set(existing_ids)
    
    try:
        #Hacemos query y devuelven pubmed_id
        Entrez.email = config.EMAIL
        handle = Entrez.esearch(db="pubmed", term=text_query, retmax=max_docs)
        response = Entrez.read(handle)
        handle.close()
        
        pubmed_id_list = response["IdList"]
        print(pubmed_id_list)
        total = len(pubmed_id_list)
        print(f"{total} studies found relating '{text_query}'")
        
        pubmed_id_list = [x for x in pubmed_id_list if f"PMID_{x}" not in eids_set]
        
        new_studies = len(pubmed_id_list)
        
        print(f"Only {new_studies} are not in our db. \nDownlaoding...")
        for i, pm_id in enumerate(pubmed_id_list):
            #Respetamos requests por segundo
            time.sleep(0.35)
            
            fetch_handle = Entrez.efetch(
                db="pubmed", 
                id=pm_id, 
                rettype="abstract", 
                retmode="text"
            )
            document_abstract = fetch_handle.read()
            fetch_handle.close()
            
            doc_id = f"PMID_{pm_id}"
            
            document_list.append((doc_id, document_abstract))
            print(f"Downloaded {i + 1}/{new_studies}")
            
        
    except Exception as e:
        print("Error descargando archivos")
        print(e)
    
    return document_list

def get_new_pubmed_sources(text_query, documents_number):
    client = chromadb.PersistentClient(path = config.VECTOR_DB_PATH)
    collection = client.get_collection(name= config.PUBMED_DOCS_COLLECTION)
    
    existing_ids = set(collection.get()['ids'])
    
    doc_list = download_studies(text_query=text_query, max_docs=documents_number, existing_ids = existing_ids)
    
    index_documents_to_db(doc_list, collection)
    
    print(f"Documents related to {text_query} indexed successfully")
    print(f"Number of final documents: {collection.count()}")
    
    return len(doc_list)
    
    
def pubmed_downloader(params):
    query = params["query"]
    doc_n = params["max_results"]
    
    indexed_docs = get_new_pubmed_sources(query, doc_n)
    
    return f"pubmed_downloader{{\"number_of_indexed_documents\": {indexed_docs}}}"