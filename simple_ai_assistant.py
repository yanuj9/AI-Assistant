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

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_DICTIONARY[func_name]

            result = fn(**func_args)

            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : str(result)
            })

        # 2nd call : Now Pass it on to LLM again -
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
        )

        msg = response.choices[0].message

    messages.append(
        {
            "role" : "assistant",
            "content" : msg.content,
        }
    )

    print("Qwen3 : ", msg.content)