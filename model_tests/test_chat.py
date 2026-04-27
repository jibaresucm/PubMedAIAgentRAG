from llama_cpp import Llama
from settings import config
import os

# Configuración técnica para tu RTX 4060
print("--- Iniciando carga del modelo Gemma 2 IQ4_XS ---")
model_path = os.path.join(config.LLM_MODELS_PATH, config.LLM_MODEL)
llm = Llama(
    model_path=model_path,
    n_ctx=65536, 
    n_gpu_layers=-1, 
    n_threads=8, 
    flash_attn=True,
    verbose=False,
    type_k=8,
    type_v= 8
)


output = llm(
        """<|turn>system Eres un asistente experto en programación.<turn|>
            <|turn>user Como se hacen las acelgas<turn|>
            <|turn>model""",
        max_tokens=512,
        stop=["<turn|>"],
        stream=False,
        echo=True
        )


text = output['choices'][0]['text']
print(text, end="", flush=True)