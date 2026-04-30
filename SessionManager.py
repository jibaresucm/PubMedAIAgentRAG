from ContextManager import ContextManager
from ModelManager import ModelManager
from ToolManager import ToolManager
from agent_settings import agent_settings


class SessionManager():
    def __init__(self):
        self.context = ""
        self.model_manager = ModelManager()
        self.context_manager = ContextManager()
        self.tool_manager = ToolManager()
        self.turn = None
        
        
        self.context += self.context_manager.add_system_prompt(agent_settings.SYSTEM_PROMPT + self.tool_manager.get_tool_descriptions())
        
    def send_prompt_to_model(self, prompt, app):
        self.context += self.context_manager.add_user_query(prompt)
        self.turn = "model"
        
        while self.turn == "model":
            
            response = ""
            for chunk in self.model_manager.run(self.context):
                app.model_new_data(chunk)
                response += chunk
            
            self.context += response
            close_reason = self.context_manager.close_reason(response)
            
            if close_reason == "user_turn":
                self.turn = "user_turn"
                self.context += "<turn|>"
                self.context = self.context_manager.clean_context(self.context)
            elif close_reason == "tool_call":
                self.turn = "model"
                calls = self.tool_manager.parse_calls(response)
                tools_responses = []
                
                for call in calls:
                    call_answer = self.tool_manager.handle_call(call)
                    tools_responses.append(call_answer)
                
                for res in tools_responses:
                    self.context += self.context_manager.add_tool_response(res)
  
            