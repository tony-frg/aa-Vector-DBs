from pymilvus import MilvusClient, model

# Set Up Vector Database
client = MilvusClient("milvus_demo.db")

# Create a Collection
if client.has_collection(collection_name="demo_collection"):
    client.drop_collection(collection_name="demo_collection")
client.create_collection(
    collection_name="demo_collection",
    dimension=768,  # The vectors we will use in this demo has 768 dimensions
)


embedding_fn = model.DefaultEmbeddingFunction()

docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

vectors = embedding_fn.encode_documents(docs)
print("Dim:", embedding_fn.dim, vectors[0].shape)  # Dim: 768 (768,)

data = [{"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"} for i in range(len(vectors))]

print("Data has", len(data), "entities, each with fields: ", data[0].keys())
print("Vector dim:", len(data[0]["vector"]))


# Insert Data
res = client.insert(collection_name="demo_collection", data=data)

print(res)

# Semantic Search
# Vector search

query_vectors = embedding_fn.encode_queries(["Who is Alan Turing?"])

res = client.search(
    collection_name="demo_collection",  # target collection
    data=query_vectors,  # query vectors
    limit=2,  # number of returned entities
    output_fields=["text", "subject"],  # specifies fields to be returned
)

print(res)


# Vector Search with Metadata Filtering

docs = [
    "Machine learning has been used for drug design.",
    "Computational synthesis with AI algorithms predicts molecular properties.",
    "DDR1 is involved in cancers and fibrosis.",
]
vectors = embedding_fn.encode_documents(docs)
data = [{"id": 3 + i, "vector": vectors[i], "text": docs[i], "subject": "biology"} for i in range(len(vectors))]

client.insert(collection_name="demo_collection", data=data)

res = client.search(
    collection_name="demo_collection",
    data=embedding_fn.encode_queries(["tell me AI related information"]),
    filter="subject == 'biology'",
    limit=2,
    output_fields=["text", "subject"],
)

print(res)

# Query

# retrieving all entities whose scalar field has a particular value:
res = client.query(
    collection_name="demo_collection",
    filter="subject == 'history'",
    output_fields=["text", "subject"],
)

print(res)

# Directly retrieve entities by primary key:
res = client.query(
    collection_name="demo_collection",
    ids=[0, 2],
    output_fields=["vector", "text", "subject"],
)

print(res)


# Delete Entities
res = client.delete(collection_name="demo_collection", ids=[0, 2])

print(res)

res = client.delete(
    collection_name="demo_collection",
    filter="subject == 'biology'",
)

print(res)

# Drop the collection
client.drop_collection(collection_name="demo_collection")
