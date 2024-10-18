import uuid
from typing import Dict, List

import chromadb.utils.embedding_functions as ef
from chr_embedding_util import CustomEmbeddingFunction
from chromadb import EmbeddingFunction, HttpClient
from chromadb.api.models.Collection import Collection

# Create a Chroma client
chroma_host = "localhost"
chroma_port = 8000
client = HttpClient(host=chroma_host, port=chroma_port)

# ================================
# CRUD Operations
# ================================


def create_collection(
    collection_name: str, documents: List[str] | None, embedding_func: EmbeddingFunction = ef.DefaultEmbeddingFunction()
) -> Collection:
    """
    Create a new collection in Chroma or retrieve an existing one, optionally adding the provided documents.
    Uses UUIDs based on timestamps for document IDs.

    Args:
        collection_name (str): The name of the collection.
        documents (Optional[List[str]]): A list of documents (strings) to add to the collection. Defaults to None.

    Returns:
        Collection: The created or retrieved collection object.

    Example:
        collection = create_collection("my_collection", ["doc1", "doc2"])
    """
    # Get or create the collection
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embedding_func)

    # Add documents if any are provided
    if documents:
        # document_ids = [f"id{idx}" for idx, _ in enumerate(documents)]
        document_ids = [str(uuid.uuid1()) for _ in documents]
        collection.add(documents=documents, ids=document_ids)
        print(f"Documents added to collection '{collection_name}'")

    return collection


def read_collection(collection: Collection, query_text: str, include_embeddings: bool = False, n_results: int = 5) -> Dict:
    """
    Query a collection for the most similar documents to the query text.

    This function queries the given collection for similar documents based on the query text.
    It can optionally include document embeddings in the result.

    Args:
        collection (Collection): The Chroma collection object to query.
        query_text (str): The search query to find similar documents.
        include_embeddings (bool, optional): Whether to include embeddings in the result. Defaults to False.
        n_results (int, optional): The number of similar results to return. Defaults to 5.

    Returns:
        Dict: A dictionary containing the query results, including documents, distances, and optionally embeddings.

    Example:
        result = read_collection(collection, "ocean content", include_embeddings=True)
    """
    include_fields = ["documents", "distances"]
    if include_embeddings:
        include_fields.append("embeddings")

    result = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=include_fields,
    )

    return result


def update_collection(collection: Collection, new_documents: List[str]) -> None:
    """
    Update a collection by adding new documents to it.

    This function adds more documents to the given collection, updating it with new content.

    Args:
        collection (Collection): The Chroma collection object to update.
        new_documents (List[str]): A list of new documents (strings) to add to the collection.

    Returns:
        None

    Example:
        update_collection(collection, ["New document content"])
    """
    document_ids = [f"id{idx}" for idx, _ in enumerate(new_documents)]
    collection.add(documents=new_documents, ids=document_ids)
    print("Collection updated with new documents")


def delete_collection(collection_name: str) -> None:
    """
    Delete a collection by name.

    This function deletes the collection with the specified name from Chroma.
    Use this operation to clean up resources.

    Args:
        collection_name (str): The name of the collection to delete.

    Returns:
        None

    Example:
        delete_collection("my_collection")
    """
    client.delete_collection(name=collection_name)
    print(f"Collection '{collection_name}' deleted")


# ================================
# Example Usage
# ================================

# Sample documents
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

# Sample documents for a new collection
new_documents = [
    "The majestic eagle soars high above the mountain peaks, scanning the terrain with sharp eyes.",
    "Under a starry sky, a lone astronomer observes distant galaxies through his telescope.",
    "The violinist pours their soul into each note, creating a symphony that touches the heart.",
    "The bustling city streets are filled with the sounds of honking cars and lively conversations.",
    "A gentle breeze rustles the leaves of the old oak tree, carrying the scent of blooming flowers.",
    "In the arctic tundra, a polar bear hunts for seals beneath the vast expanse of ice and snow.",
    "The artist splashes vivid colors on the canvas, turning imagination into a stunning landscape.",
    "The spaceship glides silently through the void, exploring the mysteries of distant planets.",
    "A baker kneads dough with care, crafting a loaf that fills the air with the aroma of fresh bread.",
    "In the deep jungle, a hidden waterfall cascades into a crystal-clear pool surrounded by lush greenery.",
]


# 1. CREATE: Add documents to a new collection
collection_name = "test_6"
collection = create_collection(collection_name, new_documents, embedding_func=CustomEmbeddingFunction())

# # Create a new collection with the new documents
# new_collection_name = "nature_and_art"
# new_collection = create_collection(new_collection_name, new_documents)


# # Get the list of collections
# collections = client.list_collections()

# # Print all available collections
# for coll in collections:
#     print(f"Collection: {coll.name}")

# 2. READ: Query the collection
query = "Give me some content about the ocean"
result = read_collection(collection, query, include_embeddings=True)

# Display query results
print(f"Query: {query}\nMost similar sentences:")
for id_, document, distance, embedding in zip(
    result["ids"][0], result["documents"][0], result["distances"][0], result.get("embeddings", [[]])[0]
):
    print(f"ID: {id_}, Document: {document}, Similarity: {1 - distance}")
    print(f"Embedding length: {len(embedding)}")
    print(f"Embedding snippet: {embedding[:5]}...")  # Print the first 5 elements of the embedding for brevity

# 3. UPDATE: Add more documents to the collection
new_documents = ["The sea turtle swims gracefully through the crystal-clear ocean."]
update_collection(collection, new_documents)

# 4. DELETE: Delete the collection (if needed)
# delete_collection(collection_name)
