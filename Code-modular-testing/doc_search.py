import os

from openai import OpenAI
from dotenv import load_dotenv
import numpy

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")

# get embeddings for a given text
def get_embedding(text):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )

    return response.data[0].embedding

# get similarity of two vectors
def cosine_similarity(A, B):
    dot_prod = numpy.dot(A,B)
    norm_a = numpy.linalg.norm(A)
    norm_b = numpy.linalg.norm(B)

    return dot_prod / (norm_a * norm_b)

# Load the documents
def load_documents(folder=KB_FOLDER):
    documents = []

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source" : filename,
                    "text" : f.read()
                }
            )

    return documents

# Add embeddings in the documents
def add_embedding(documents):
    for document in documents:
        vector = get_embedding(document["text"])
        document["vector"] = vector

    return documents

# Search method to search the top_k documents for a user_query
def search(query, documents, top_k=3):
    query_vector = get_embedding(query)

    results = []
    for document in documents:
        score = cosine_similarity(query_vector, document["vector"])
        results.append(
            {
                "score" : float(score),
                "source" : document["source"],
                "text" : document["text"],
                "size" : len(document["text"])
            }
        )

    results.sort(key=lambda rec:rec["score"], reverse=True)
    return results[:top_k]

# Testing Method
def test(user_query, documents,top_k=3):
    print(f"\nUser Query: {user_query}")

    results = search(user_query, documents,top_k)

    for r in results:
        print(f"{r['score']:.2f} - {r['source']} - {r['size']} characters")


documents = load_documents()
documents = add_embedding(documents)

print(f"{len(documents)} documents embedded")
user_query = "How many days will I get for maternity leave ?"
test(user_query=user_query, documents=documents,top_k=3)