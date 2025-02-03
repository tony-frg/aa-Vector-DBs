# import uuid
from typing import Dict, List, Literal, Optional

import chromadb.utils.embedding_functions as ef
from chr_embedding_util import CustomEmbeddingFunction
from chromadb import EmbeddingFunction, HttpClient, Metadata
from chromadb.api.models.Collection import Collection
from chromadb.api.types import OneOrMany

from src.config import settings

# ================================
# CRUD Operations
# ================================


def create_collection(
    collection_name: str,
    documents: Optional[List[str]] = None,
    docs_metadatas: Optional[OneOrMany[Metadata]] = None,
    distance_function: Literal["cosine", "ip", "l2"] = "cosine",
    embedding_func: Optional[EmbeddingFunction] = ef.DefaultEmbeddingFunction(),
) -> Collection:
    """
    Create or retrieve a collection in Chroma, optionally adding provided documents to it. Document IDs are
    generated as UUIDs based on timestamps.

    Args:
        collection_name (str): The name of the collection to create or retrieve.
        documents (Optional[List[str]], optional): A list of document strings to add to the collection.
            Defaults to None.
        docs_metadatas (Optional[OneOrMany[Metadata]], optional): Metadata corresponding to each document
            (either one metadata per document or shared metadata for all). Defaults to None.
        distance_function (str, optional): The distance function for similarity search (e.g., "cosine").
            Defaults to "cosine".
        embedding_func (Optional[EmbeddingFunction], optional): The embedding function used to convert documents
            into vector representations. Defaults to the DefaultEmbeddingFunction.

    Returns:
        Collection: The created or retrieved Chroma collection object.

    Example:
        collection = create_collection(
            "my_collection",
            documents=["doc1", "doc2"],
            docs_metadatas=[{"type": "example"}]
        )
    """
    # Get or create the collection
    collection = client.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": distance_function}, embedding_function=embedding_func
    )

    # Add documents if any are provided
    if documents:
        document_ids = [f"id{idx}" for idx, _ in enumerate(documents)]
        # document_ids = [str(uuid.uuid1()) for _ in documents]
        collection.add(
            ids=document_ids,
            metadatas=docs_metadatas,
            documents=documents,
        )
        print(f"Documents added to collection '{collection_name}'")

    return collection


def read_collection(
    collection: Collection,
    query_text: str,
    include_embeddings: bool = False,
    n_results: int = 5,
) -> Dict:
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
    include_fields = ["documents", "distances", "metadatas"]
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

# Create a Chroma client
chroma_host = settings.chroma_host
chroma_port = settings.chroma_port
client = HttpClient(host=chroma_host, port=chroma_port)

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

# Corresponding metadata for the documents
docs_metadatas = [
    {
        "title": "Tropical Adventures of Parrots",
        "author": "Jane Wildlife",
        "tags": "nature",
        "publication_date": "2023-06-15",
        "views": 250,
    },
    {
        "title": "Mathematical Patterns of the Universe",
        "author": "Albert Numbers",
        "tags": "mathematics",
        "publication_date": "2022-11-20",
        "views": 1200,
    },
    {
        "title": "Efficiency in Robotics",
        "author": "Robo Innovator",
        "tags": "technology",
        "publication_date": "2024-03-10",
        "views": 1800,
    },
    {"title": "Culinary Masterpieces", "author": "Chef Gourmet", "tags": "cooking", "publication_date": "2023-01-25", "views": 950},
    {
        "title": "Secrets of the Ancient Tree",
        "author": "Nature Lover",
        "tags": "nature",
        "publication_date": "2023-09-30",
        "views": 600,
    },
    {
        "title": "Detective's Intricate Clues",
        "author": "Sherlock Chronicles",
        "tags": "mystery",
        "publication_date": "2022-12-18",
        "views": 1300,
    },
    {"title": "Colors of the Sunset", "author": "Sky Painter", "tags": "nature", "publication_date": "2023-07-12", "views": 1100},
    {
        "title": "Symphony of the Forest",
        "author": "Wilderness Explorer",
        "tags": "nature",
        "publication_date": "2023-08-05",
        "views": 900,
    },
    {
        "title": "Expressive Dance Stories",
        "author": "Grace Performer",
        "tags": "art",
        "publication_date": "2024-01-22",
        "views": 750,
    },
    {
        "title": "Quantum Particles' Dance",
        "author": "Physicist Pro",
        "tags": "science",
        "publication_date": "2023-11-11",
        "views": 1400,
    },
]


# Sample documents for a new collection
# new_documents = [
#     "The majestic eagle soars high above the mountain peaks, scanning the terrain with sharp eyes.",
#     "Under a starry sky, a lone astronomer observes distant galaxies through his telescope.",
#     "The violinist pours their soul into each note, creating a symphony that touches the heart.",
#     "The bustling city streets are filled with the sounds of honking cars and lively conversations.",
#     "A gentle breeze rustles the leaves of the old oak tree, carrying the scent of blooming flowers.",
#     "In the arctic tundra, a polar bear hunts for seals beneath the vast expanse of ice and snow.",
#     "The artist splashes vivid colors on the canvas, turning imagination into a stunning landscape.",
#     "The spaceship glides silently through the void, exploring the mysteries of distant planets.",
#     "A baker kneads dough with care, crafting a loaf that fills the air with the aroma of fresh bread.",
#     "In the deep jungle, a hidden waterfall cascades into a crystal-clear pool surrounded by lush greenery.",
# ]


# 1. CREATE: Add documents to a new collection
collection_name = "test_collection"

openai_ef = ef.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name=settings.openai_embedding_model,
)

sentence_transformer_ef = ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

my_custom_ef = CustomEmbeddingFunction()


oaief_collection = create_collection(collection_name + "_" + "opeanai", documents, docs_metadatas, embedding_func=openai_ef)

stef_collection = create_collection(
    collection_name + "_" + "sent_transf", documents, docs_metadatas, embedding_func=sentence_transformer_ef
)

custef_collection = create_collection(collection_name + "_" + "cust_ef", documents, docs_metadatas, embedding_func=my_custom_ef)

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

result = read_collection(oaief_collection, query, include_embeddings=False)


# # Display query results
# print(f"Query: {query}\nMost similar sentences:")
# for id_, document, metadatas, distance, embedding in zip(
#     result["ids"][0], result["documents"][0], result["metadatas"], result["distances"][0], result.get("embeddings", [[]])[0]
# ):
#     print(f"ID: {id_}, Document: {document}, Similarity: {1 - distance}")
#     print(f"Embedding length: {len(embedding)}")
#     print(f"Metadatas: {metadatas}")
#     print(f"Embedding snippet: {embedding[:5]}...")  # Print the first 5 elements of the embedding for brevity


# Metadata Filters and Document Filters
wh_doc = {"$contains": "adventures"}
wh_mtdt = {"tags": {"$eq": "nature"}}

# print(oaief_collection.query(query_texts=query, where_document=wh_doc, where=wh_mtdt))


# # 3. UPDATE: Add more documents to the collection
# new_documents = ["New collection"]
# update_collection(oaief_collection, new_documents)

# # switch `add` to `upsert` to avoid adding the same documents every time
# oaief_collection.upsert(
#     documents=[
#         "This is a new document",
#         "This is a document about strawberries"
#     ],
#     ids=["id1", "id3"]
# )

# 4. DELETE: Delete the collection (if needed)
delete_collection(oaief_collection.name)
