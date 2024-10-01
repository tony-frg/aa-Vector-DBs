# aa-Vector-Databases CRUD Examples

This repository provides examples of how to use **vector databases** for storing and querying high-dimensional vector
data. It includes basic **CRUD operations** (Create, Read, Update, Delete) using two popular vector databases:
- **Chroma DB**
- **pgVector** (Postgres with the `pgvector` extension)

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Devcontainer Setup](#devcontainer-setup)
  - [Running Python Scripts in Devcontainer](#running-python-scripts-in-devcontainer)
- [Chroma DB Examples](#chroma-db-examples)
  - [CRUD Operations](#crud-operations-for-chroma-db)
- [pgVector Examples](#pgvector-examples)
  - [CRUD Operations](#crud-operations-for-pgvector)
- [Usage](#usage)
  - [Running ChromaDB CRUD Operations](#running-chromadb-crud-operations)
  - [Running pgVector CRUD Operations](#running-pgvector-crud-operations)
- [Database Access](#database-access)


## Introduction

Vector databases are specialized data stores optimized for handling vectors, commonly used in AI/ML applications for
tasks such as semantic search, embeddings, and similarity searches. This repository demonstrates how to:
- Store vector data
- Retrieve and query vectors
- Update vectors
- Delete vectors

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/) for running services locally
- [Python 3.10+](https://www.python.org/) for running Python code
- [PostgreSQL](https://www.postgresql.org/) (with `pgvector` extension)
- [Visual Studio Code](https://code.visualstudio.com/Download) for working with **devcontainers**

## Setup

* Clone the repository:
    ```bash
    git clone https://github.com/tony-frg/aa-Vector-DBs.git
    cd aa-Vector-DBs
    ```
* Create a virtualenv:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

* Install Python Dependencies via:
  ```bash
  make install-dev
  ```
  This will install dependencies listed in the `requirements-dev.txt` file, which include libraries like `psycopg2` for
  PostgreSQL and `chromadb` for Chroma DB.

### Devcontainer Setup

To run the Python code from inside a **devcontainer**, make sure you have Docker and Visual Studio Code with the
**Remote - Containers** extension installed.

1. Open the project folder in Visual Studio Code.
2. Visual Studio Code will detect the `.devcontainer` configuration and prompt you to "**Reopen in Container**".
Click this option.
3. The devcontainer setup will automatically build and launch the Docker environment defined in `docker-compose.yaml`.

Inside the container, the workspace is mounted at `/usr/repos/aa-Vector-DBs`.

Once the containers are up, you'll have access to:
- **ChromaDB** running at `localhost:8000`
- **pgvector** running at `localhost:5433`
- **Vector Admin** running at `localhost:3001`
- A development container for running Python code

### Running Python Scripts in Devcontainer
Once the devcontainer is running:

1. Open a terminal within VS Code (inside the devcontainer).
2. Run any Python script. For example:
    ```bash
    python src/pgvector_examples/pgvector_crud.py
    ```

## Chroma DB Examples

**Chroma DB** is a vector database that is designed for fast and efficient storage and retrieval of high-dimensional
vector embeddings.

### CRUD Operations for Chroma DB

- **Create**: Insert vector data into the Chroma DB.
- **Read**: Query vectors using similarity search.
- **Update**: Modify existing vectors.
- **Delete**: Remove vectors from the database.

You can find the code examples in the [`src/chroma_db_examples/`](src/chroma_db_examples) directory.

## pgVector Examples

**pgVector** is an extension for PostgreSQL that adds support for vector data types. It allows you to store and query
vectors in a relational database.

### CRUD Operations for pgvector

- **Create**: Insert vector data into a `pgvector` table.
- **Read**: Query vectors using Postgres SQL with similarity functions.
- **Update**: Modify vectors in a `pgvector` column.
- **Delete**: Remove vectors from the table.

Examples are located in the [`src/pgvector_examples`](src/pgvector_examples) directory.

## Usage
After setting up the environment and the devcontainer, you can run the following example scripts:

### Running ChromaDB CRUD Operations
To run the ChromaDB CRUD operations:
```bash
python src/chroma_db_examples/chroma_crud.py
```

This will demonstrate how to:

- Create a collection and add documents to it
- Perform similarity search queries
- Update and delete collections

### Running pgVector CRUD Operations
To run the pgVector CRUD operations:

```bash
python src/pgvector_examples/pgvector_crud.py
```

This will execute:

- Insertion of vectors into the `pgvector` table
- Perform similarity searches using `pgvector`
- Update and delete vector data

## Database Access
Once your Docker containers are running, you can access the databases using these URLs:

- ChromaDB: http://localhost:8000
- pgVector (PostgreSQL): Use any PostgreSQL client (e.g., DBeaver) with the following settings:
- Host: `localhost`
- Port: `5433`
- Database: `mydb`
- User: `myuser`
- Password: `mypassword`
If you're using Vector Admin, it will be available at http://localhost:3001.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
