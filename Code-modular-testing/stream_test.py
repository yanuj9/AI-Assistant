import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

stream = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[{"role" : "user", "content" : "Explain python in 100 words. No need to mention words count. "}],
    stream=True
)

full_response = ""

for chunk in stream:

    if not chunk.choices:
        continue

    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True) # Python keeps the stream data in buffer and prints them in batches, flush = True fixes it
        full_response += piece

print("\nFull response : ")
print(full_response)