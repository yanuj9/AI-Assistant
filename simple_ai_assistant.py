from openai import OpenAI
from dotenv import load_dotenv
import os

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
        messages=messages
    )

    messages.append(
        {
            "role" : "assistant",
            "content" : response.choices[0].message.content,
        }
    )

    print("Qwen3 : ", response.choices[0].message.content)
    # print(response.choices[0].message.role)

# print("LLM Response : ")
# print(response)
# print(response.choices[0].message.content) # Response from qwen3:4b