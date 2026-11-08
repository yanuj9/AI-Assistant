import json
from datetime import datetime
import requests
from rag import search

from Utilities.utilities import log

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_user_city():
    return "Bangalore"

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url=url, timeout=10)
    response.raise_for_status() # raises HTTPerror if something went wrong
    return response.text

def search_knowledge_base(query):
    results = search(query, top_k=2)

    log(f"📚 Knowledge base search : {query}")
    for r in results:
        log(f"   {r['score']:.2f} - {r['source']} #{r['chunk_id']}")

    blocks = []

    for r in results:
        sourceFileName = r['source'],
        chunkId = r['chunk_id'],
        chunkTest = r['text']

        header = f"[{sourceFileName} #{chunkId}]"
        block = f"{header}\n{chunkTest}"
        blocks.append(block)

    return "\n\n".join(blocks)

# Tools = [{}, {}, ..., {}]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description" : "Returns the current date and time as a formatted string.",
            "parameters": {
                "type" : "object",
                "properties" : {
                    # "city" : {
                    #     "type" : "string",
                    #     "description" : "The name of the city"
                    # }
                }
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_city_weather",
            "description" : "Returns the live weather of a given city",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "City for which the weather is asked"
                    }
                },
                "required" : ["city"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_user_city",
            "description" : "Returns the city where user lives. Use this when the user says 'my city', 'where I live', 'my home', 'my location' without naming the city",
            "parameters" : {
                "type" : "object",
                "properties" : {}
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "search_knowledge_base",
            "description" : "Searches the Zorvex Technologies company knowledge base: leave, medical, HR, Hiring, tech, incident "
                            "reports and travel expense policies. Use it for any question about company policies or documentation"
                            "Returns the most relevant passages with their source.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "The user's question, rewritten as a short, self-contained search query"
                    }
                },
                "required" : ["query"]
            }
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_DICTIONARY = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city,
    "search_knowledge_base" : search_knowledge_base
}

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    
    try : 
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"🔧{func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_DICTIONARY[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running {func_name} : {e}"
    
    log(f"   ↳{result}")

    return str(result)