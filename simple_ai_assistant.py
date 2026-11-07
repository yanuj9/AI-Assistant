# standard library imports
import os
from types import SimpleNamespace

# Third-party imports
from openai import OpenAI
from dotenv import load_dotenv

# Local imports
from Utilities.utilities import log
from tools import TOOLS, run_tool


"""
Whatever we provide to the model is a Hint not a guarantee.
Small models may still ignore instructions.
So make it a habit to not rely on model totally. (graceful Exception handling)
"""



"""
Streaming : Improving the time to see the first word (seems fast to user)

First word appears in 1 - 2 seconds (TTFT : Time to First Token)
Vs
10 seconds to see full response 
"""

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
        "content" : "You're a general-purpose assistant. Answer questions using your knowledge. Use the provided tools only when they help with the request. The tools do not limit what you can answer. If you don't know something, say so. Keep your answers in 200 words"
    }
)

def stream_chat(history):
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools=TOOLS,
        stream=True
    )

    full_response = ""
    calls = {}
    icon_printed = False

    try:
        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # Content Streaming
            if delta.content:
                if not icon_printed:
                    print("🤖 Qwen3 : ", end = "", flush=True)
                    icon_printed = True
                print(delta.content, end="", flush=True)
                full_response += delta.content

            # Tool calling
            for tc in (delta.tool_calls or []):
                obj = calls.setdefault(
                    tc.index,
                    SimpleNamespace(id = None, function=SimpleNamespace(name="", arguments="")),
                )

                if tc.id:
                    obj.id = tc.id
                if tc.function and tc.function.name:
                    obj.function.name += tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments += tc.function.arguments

    except KeyboardInterrupt:
        print("\nStopped by You, exiting the chat.")
        calls = {}
        

    if icon_printed:
        print()

    call_list = []

    for key in sorted(calls):
        call_list.append(calls[key])

    return full_response, call_list

def build_tool_calls_payload(tool_calls):
    """ converts out collected tools calls in the dict format as API expects """

    payload = []

    for tool_call in tool_calls:
        tool_call_dict = {
            "id" : tool_call.id,
            "type" : "function",
            "function" : {
                "name" : tool_call.function.name,
                "arguments" : tool_call.function.arguments,
            },
        }
        payload.append(tool_call_dict)

    return payload


while True:
    user_input = input("\n👦🏻 Anuj : ")

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

        full_response, tool_calls = stream_chat(messages)

        if not tool_calls:
            break

        log(f"Step {step + 1}: model requested {len(tool_calls)} tool calls")
        
        messages.append({
            "role" : "assistant",
            "content" : full_response,
            "tool_calls" : build_tool_calls_payload(tool_calls)
        })

        for tool_call in tool_calls:
            result = run_tool(tool_call)

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
        print("🤖 Qwen3 : ", fallback)
        continue