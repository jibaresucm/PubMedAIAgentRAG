from create_models import get_llm_model

class ModelManager():
    
    def __init__(self):
        self.llm = get_llm_model()
    
    def run(self, context):
        new_context = ""
        stream = self.llm(
                context,
                max_tokens=4096,
                stop=["<turn|>", "<|tool_response>", "<eos>"],
                stream=True,
                echo=False
            )
        
        for chunk in stream:
            generated = chunk['choices'][0]['text']
            
            new_context += generated
            
            yield generated
