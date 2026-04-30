import json
import re
from pubmed_downloader import pubmed_downloader
from studies_rag import studies_rag

tools = {
    "pubmed_downloader" :{
        "name": "pubmed_downloader",
        "description": "Descarga abstracts de estudios PubMed (biomedicina) y los indexa en una base de datos vectorial accesible con la herramienta 'studies_rag'. No devuelve los estudios, solo los indexa a la abse de datos.",
        "use_description": "Usa esta herramienta cuando necesites investigar temas biomédicos específicos o ampliar información sobre un tema más especifico (como el que usa una lupa sobre un mapa que ya estaba mirando). La busqueda deberá utilizar un lenguaje técnico especifico al campo que se esta estudiando y deberá de ser adaptado para obtener resultados acerca de un tema (que confirmen el sesgo del usuario o lo desmienta). Es obligatorio utilizar el inglés al describir la búsqueda. Tras usar esta herramienta tendrás que usar studies_rag para recibir la información. Si no descarga ningún documento significa que ya estaba en la base de datps",
        "parameters": {
        "type": "object",
        
        "properties": {
            "query": {
                "type": "string",
                "description": "La cadena de búsqueda en inglés para realizar en PubMed."
            },
            "max_results": {
                "type": "integer",
                "description": "Número máximo de estudios a recuperar (20 por defecto, se recomiendan unos 40)."
            }
        },
        
        "required": ["query"]
        
        },
        "call_example": '<|tool_call>call:pubmed_downloader{query:<|"|>impact of intermittent fasting on insulin resistance<|"|>, max_results:15}<tool_call|>',
        "function": pubmed_downloader
    },
    
    "studies_rag" :{
        "name": "studies_rag",
        "description": "Recoge abstracts de estudios (previamente descargados) de una base de datos vectorial.",
        "use_description": "Utilizarás esta herramienta para obtener información acerca de un tema en concreto que se este discutiendo con el usuario. La query a la base de datos tendrá que estár optimizada para que su embedding sea cercano a información que queremos obtener. Es decir no solamente lo utilices como una búsqueda, detalla en la query las afirmaciones que quieras encontrar en los estudios. La query se realizará en inglés. La fuente de la información es el id del documento, no la herramienta en si"
,
        "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "La pregunta o concepto clave convertido a lenguaje de consulta para la búsqueda vectorial. Deberá imitar la informacion que queremos encontrar para que el modelo de embeddings lo asocie con documentos que tenga informacion parecida, que no sea una pregunta si no afirmaciones o simplemente texto sin subjetividad. Mantenlo corto, no añadas más información de la que se te pide solo traducela al inglés usando palabras adecuadas."
            },
            "max_results": {
                "type": "integer",
                "description": "Número de fragmentos de estudio a recuperar (10 por defecto)."
            }
        },
        "required": ["query"]
    },
        "call_example": '<|tool_call>call:studies_rag{query:<|"|>the effect of fasting on insulin sensitivity was found to be<|"|>, max_results:5}<tool_call|>',
        "function": studies_rag
    }
}

class ToolManager():
    
    def handle_call(self, call_tuple):
        tool_name = call_tuple[0]
        params = call_tuple[1]
        
        received_params = params.keys()
        required_params = tools[tool_name]["parameters"]["required"]
        
        all_required_included = set(required_params).issubset(set(received_params))
        
        ret = None
        if all_required_included:
            ret = tools[tool_name]["function"](params)
        else:
            print("No se ha podido realizar la llamada")
        
        return ret
    
    def get_tool_descriptions(self):
        start_token = "\n<|tool>\n"
        end_token = "\n<tool|>\n"
        
        tools_desc = "\n Estas son las herramientas que tienes disponibles\n"
        
        for id, tool in tools.items():
            tools_desc += start_token
            
            tools_desc += tool["name"] + "\n\n"
            tools_desc += tool["description"] + "\n\n"
            tools_desc += tool["use_description"] + "\n\n"
            
            parameters = tool["parameters"]
            parameters_str = json.dumps(parameters, indent=4, ensure_ascii=False)
            tools_desc += "Parametros (JSON)" + parameters_str + "\n\n"
            
            tools_desc += "Ejemplo de llamada:" + tool["call_example"] + "\n"
            
            tools_desc += end_token
        return tools_desc

    def parse_calls(self, response):
        pattern = r"<\|tool_call>call:(\w+)\{(.*?)\}<tool_call\|>"
        matches = re.findall(pattern, response, re.DOTALL)
        
        matches = [m for m in matches if len(m[0]) != 0]
        
        print(matches)
        
        calls = []
        for call in matches:
            tool_name = call[0]
            parameters = call[1].split(",")
            parameters = [x.strip().replace('<|"|>', "").split(":") for x in parameters]
            parameters = [x for x in parameters if len(x) == 2]
            
            param_prop = tools[tool_name]["parameters"]["properties"]
            
            param_dict = {}
            for elem in parameters:
                if(param_prop[elem[0]]["type"] == "string"):
                    param_dict[elem[0]] = elem[1]
                
                elif(param_prop[elem[0]]["type"] == "integer"):
                    param_dict[elem[0]] = int(elem[1])

            calls.append((tool_name, param_dict))
        
        return calls
            
        


tm = ToolManager()