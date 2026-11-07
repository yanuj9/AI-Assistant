import os

import numpy
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # by default looks for .env file and loads all of these in environment variables

# Pooling is creating an embedding vector for the entire given string
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.environ["API_KEY"]
)

def get_embedding(text):
    response = client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A, B):
    dot_prod = numpy.dot(A,B)
    norm_a = numpy.linalg.norm(A)
    norm_b = numpy.linalg.norm(B)

    return dot_prod / (norm_a * norm_b)

text1 = "Python is a programming language"
text2 = "Python is used to write AI related code snippets"
text3 = "I love eating apples every morning"

embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)

similarity12 = cosine_similarity(embedding1, embedding2)
similarity13 = cosine_similarity(embedding1, embedding3)
similarity32 = cosine_similarity(embedding3, embedding2)

print("Similarity between text1 and text2 : ", f"{similarity12:.2f}")
print("Similarity between text2 and text3 : ", f"{similarity32:.2f}")
print("Similarity between text1 and text3 : ", f"{similarity13:.2f}")
