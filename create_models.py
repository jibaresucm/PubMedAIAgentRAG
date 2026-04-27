from llama_cpp import Llama
from settings import config
import os

llm = None

def get_llm_model():
    
    global llm
    
    if llm == None :
        model_path = os.path.join(config.LLM_MODELS_PATH, config.LLM_MODEL)
        
        llm = Llama(
            model_path=model_path,
            n_ctx=config.LLM_CONTEXT, 
            n_gpu_layers=-1, 
            n_threads=8, 
            flash_attn=True,
            verbose=False,
        )
    
    return llm

emb = None

def get_embedding_model():
    
    global emb
    
    if emb == None:
        model_path = os.path.join(config.EMBEDDING_MODELS_PATH, config.EMBEDDING_MODEL)
        
        emb = Llama(
            model_path=model_path,
            n_ctx=config.EMBEDDING_CONTEXT, 
            n_gpu_layers=-1, 
            n_threads=8, 
            flash_attn=True,
            embedding= True,
            verbose=False,
        )
    
    return emb