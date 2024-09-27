from chr_embedding_util import CustomEmbeddingFunction
from chromadb import HttpClient

# Create a Chroma client
client = HttpClient(host="chromadb", port=8000)

# Testing to ensure that the chroma server is running
print("HEARTBEAT:", client.heartbeat())

# Get a collection object from an existing collection, by name. If it doesn't exist, create it.
collection = client.get_or_create_collection(name="test", embedding_function=CustomEmbeddingFunction())

# Get the list of collections
collections = client.list_collections()

# Print all available collections
for coll in collections:
    print(f"Collection: {coll.name}")


documents = [
    "A group of vibrant parrots chatter loudly, sharing stories of their tropical adventures.",
    "The mathematician found solace in numbers, deciphering the hidden patterns of the universe.",
    "The robot, with its intricate circuitry and precise movements, assembles the devices swiftly.",
    "The chef, with a sprinkle of spices and a dash of love, creates culinary masterpieces.",
    "The ancient tree, with its gnarled branches and deep roots, whispers secrets of the past.",
    "The detective, with keen observation and logical reasoning, unravels the intricate web of clues.",
    "The sunset paints the sky with shades of orange, pink, and purple, reflecting on the calm sea.",
    "In the dense forest, the howl of a lone wolf echoes, blending with the symphony of the night.",
    "The dancer, with graceful moves and expressive gestures, tells a story without uttering a word.",
    "In the quantum realm, particles flicker in and out of existence, dancing to the tunes of probability.",
]

# Every document needs an id for Chroma
document_ids = list(map(lambda tup: f"id{tup[0]}", enumerate(documents)))

collection.add(documents=documents, ids=document_ids)

query = "Give me some content about the ocean"

# Include the source document and the Cosine Distance in the query result
result = collection.query(
    query_texts=[query],
    n_results=5,
    include=["documents", "distances", "embeddings"],
)

print("Query:", query)
print("Most similar sentences:")
# Extract the first (and only) list inside 'ids'
ids = result.get("ids")[0]
# Extract the first (and only) list inside 'documents'
documents = result.get("documents")[0]
# Extract the first (and only) list inside 'distances'
distances = result.get("distances")[0]
# Extract the first (and only) list inside 'embeddings'
embeddings = result.get("embeddings")[0]

for id_, document, distance, embedding in zip(ids, documents, distances, embeddings):
    # Cosine Similiarity is calculated as 1 - Cosine Distance
    print(f"ID: {id_}, Document: {document}, Similarity: {1 - distance}")
    # print(f"embedding length: {len(embedding)}")
    # print(f"Embedding: {embedding[:10]}...")  # Print the first 5 elements of the embedding for brevity
