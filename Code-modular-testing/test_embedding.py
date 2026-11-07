import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # by default looks for .env file and loads all of these in environment variables

# Pooling is creating an embedding vector for the entire given string
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.environ["API_KEY"]
)

response = client.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    input=["I am a good boy", "python is a good language", "He is a good coder"]
)

for i, emb in enumerate(response.data):
    print(f"Embedding {i} length : {len(emb.embedding)}")
    print(emb.embedding[:2])