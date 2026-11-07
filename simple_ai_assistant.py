from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_DICTIONARY
import os
import json

load_dotenv() # by default looks for .env file and loads all of these in environment variables

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.environ["API_KEY"]
)

messages = []

# Max limit of round of tools called for user's one question
MAX_STEPS = 5

messages.append(
    {
        "role" : "system",
        "content" : "Act like a very humble agent but and respond always under 40 words."
    }
)

while True:
    user_input = input("\nAnuj : ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append(
        {
            "role" : "user",
            "content" : user_input,
        }
    )

    # Chained tool call (Also called -> Agent Loop)

    # Chained / Sequential tool calling can run indefintely -> fixed here by for loop with range()
    # First wrong answer will cascade
    # small models struggle with multi-step planning, can also call tools in the wrong order
    # Since LLM is non deterministic, it becomes difficult to debug
    # Prompt injection is a threat, installed by external users (malicious)

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools=TOOLS
            )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break
        
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            try : 
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_DICTIONARY[func_name]
                result = fn(**func_args)
            except Exception as e:
                result = f"Error while running {func_name} : {e}"

            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : str(result)
            })

    # else block in python for a for loop runs only when loop does not end normally
    else :
        fallback = "Sorry, I could not finish this within step limit."
        messages.append({
            "role" : "assistant",
            "content" : fallback
        })
        print("Qwen3 : ", fallback)
        continue

    messages.append(
        {
            "role" : "assistant",
            "content" : msg.content,
        }
    )

    print("Qwen3 : ", msg.content)