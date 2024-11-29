# import uuid
from typing import Dict, List, Literal, Optional

import chromadb.utils.embedding_functions as ef
from chr_embedding_util import MyCustomEmbeddingFunction
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


def query_collection(
    collection: Collection,
    query_text: str | None = None,
    query_embedding: List[List[float]] | None = None,
    doc_ids: List[str] | None = None,
    n_results: int = 5,
    where_metadata: Dict[str, str] | None = None,
    include_fields: List[str] | None = None,
) -> Dict:
    """
    Query a Chroma collection for the most similar documents based on specified criteria.

    If both `doc_ids` and query parameters are provided, the function will return both:
    - The documents specified by `doc_ids`.
    - The results of the similarity query based on `query_text` or `query_embedding`.

    This allows for flexible retrieval of documents, enabling users to get specific documents while also exploring related content.

    Args:
        collection (Collection): The Chroma collection object to query.
        query_text (Optional[str]): The text to use for finding similar documents. Defaults to None.
        query_embedding (Optional[List[List[float]]]): A precomputed embedding for the query, used
            instead of `query_text` if provided. Defaults to None.
        doc_ids (Optional[List[str]]): A list of specific document IDs to retrieve directly. Defaults to None.
        n_results (int): The number of most similar results to return. Defaults to 5.
        where_metadata (Optional[Dict[str, str]]): Key-value pairs to filter results by document metadata.
            Defaults to None.
        include_fields (List[str], optional): A list of what to include in the results.
            Can contain `"embeddings"`, `"metadatas"`, `"documents"`, `"distances"`. Ids are always included.
            Defaults to `["metadatas", "documents", "distances"]`.

    Returns:
        Dict: A dictionary containing the query results with the specified fields.

    Example:
        result = read_collection(
            collection,
            query_text="ocean content",
            include_fields=["documents", "distances", "metadatas"]
        )
    """
    # Set default fields if none are specified
    if include_fields is None:
        include_fields = ["documents", "distances", "metadatas"]

    # Retrieve results based on document IDs
    results = {}
    if doc_ids:
        results["documents"] = collection.get(ids=doc_ids)

    # Retrieve results based on query parameters
    if query_text or query_embedding:
        results["query_results"] = collection.query(
            query_embeddings=query_embedding,
            query_texts=[query_text] if query_text else None,
            n_results=n_results,
            where=where_metadata,
            include=include_fields,
        )

    return results


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
    try:
        client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted")
    except ValueError as error:
        print(f"Error: {error}")


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
collection_name = "test_collection"

openai_ef = ef.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name=settings.openai_embedding_model,
)

sentence_transformer_ef = ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

my_custom_ef = MyCustomEmbeddingFunction()


oaief_collection = create_collection(collection_name + "_" + "opeanai", new_documents, embedding_func=openai_ef)
stef_collection = create_collection(collection_name + "_" + "sent_transf", new_documents, embedding_func=sentence_transformer_ef)
custef_collection = create_collection(collection_name + "_" + "cust_ef", new_documents, embedding_func=my_custom_ef)

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
result = query_collection(collection=oaief_collection, query_text=query, include_fields=["documents", "distances", "metadatas"])

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
update_collection(oaief_collection, new_documents)

# 4. DELETE: Delete the collection (if needed)
# delete_collection(collection_name)
