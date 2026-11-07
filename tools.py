from datetime import datetime
import requests

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_user_city():
    return "Bangalore"

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url=url, timeout=10)
    return response.text

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
                }
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
    }
]

FUNCTION_NAME_TO_FUNCTION_DICTIONARY = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city
}
