class ContextManager():
    
    def clean_context(self, context):
        start_token = "<|channel>thought"
        end_token = "<channel|>"
        
        while True:
            start_idx = context.find(start_token)
            
            if start_idx == -1:
                break
                
            end_idx = context.find(end_token, start_idx)
            
            if end_idx == -1:
                context = context[:start_idx]
                break
                
            context = context[:start_idx] + context[end_idx + len(end_token):]
            context = context.strip()
            
        return context
    
    def add_user_query(self, content):
        start_token = "\n<|turn>user\n"
        end_token = "\n<turn|>\n<|turn>model\n"
        ret = start_token + content + end_token
        
        return ret
    
    def add_tool_response(self, content):
        start_token = "\n<|tool_response>response:"
        end_token = "<tool_response|>\n"
        #Content debe de estar formateado
        ret = start_token + content + end_token
        
        return ret
    
    def close_reason(self, response):
        
        if "<tool_call|>" in response:
            return "tool_call"
        else: return "user_turn"
    
    def add_system_prompt(self, content):
        start_token = "\n<|turn>system\n"
        end_token = "\n<turn|>"
        ret = start_token + content + end_token
        
        return ret
    
