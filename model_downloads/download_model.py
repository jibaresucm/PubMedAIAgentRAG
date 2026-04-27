from huggingface_hub import hf_hub_download
import os
from settings import config

def download_llm_model(model_id, model_path, model_name):
    print(f"Descargando el modelo {model_id}")
    
    final_path = hf_hub_download(
        repo_id=model_id,
        filename=model_name,
        local_dir=model_path,
        local_dir_use_symlinks=False
    )
    
    print(f"Descargado en {final_path}")

model_id = "jinaai/jina-embeddings-v5-text-small-retrieval-GGUF"
model_path = config.EMBEDDING_MODELS_PATH
model_name = "v5-small-retrieval-IQ4_NL.gguf"

download_llm_model(model_id, model_path, model_name)