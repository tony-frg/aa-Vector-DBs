# aa-Vector-Databases CRUD Examples

This repository provides examples of how to use **vector databases** for storing and querying high-dimensional vector data. It includes basic **CRUD operations** (Create, Read, Update, Delete) using two popular vector databases:
- **Chroma DB**
- **pgvector** (Postgres with the `pgvector` extension)

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Chroma DB Examples](#chroma-db-examples)
  - [CRUD Operations](#crud-operations-for-chroma-db)
- [pgvector Examples](#pgvector-examples)
  - [CRUD Operations](#crud-operations-for-pgvector)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Vector databases are specialized data stores optimized for handling vectors, commonly used in AI/ML applications for tasks such as semantic search, embeddings, and similarity searches. This repository demonstrates how to:
- Store vector data
- Retrieve and query vectors
- Update vectors
- Delete vectors

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/) for running services locally
- [Python 3.10+](https://www.python.org/) for running Python code
- [PostgreSQL](https://www.postgresql.org/) (with `pgvector` extension)

## Setup

### Clone the repository

```commandline
git clone https://github.com/your-username/vector-dbs-crud.git
cd vector-dbs-crud
```

### Install Python Dependencies

Make sure you have `make` installed and run the following command to install necessary Python libraries:


This will install dependencies listed in the `requirements-dev.txt` file, which include libraries like `psycopg2` for PostgreSQL and `chromadb` for Chroma DB.

### Running with Docker

For easy setup, we provide a `docker-compose-test.yaml` file that sets up both **pgvector** and your development environment.

```commandline
make run-image
```

Once the containers are up, you'll have access to:
- **pgvector** running at `localhost:5433`
- A development container for running Python code

## Chroma DB Examples

**Chroma DB** is a vector database that is designed for fast and efficient storage and retrieval of high-dimensional vector embeddings.

### CRUD Operations for Chroma DB

- **Create**: Insert vector data into the Chroma DB.
- **Read**: Query vectors using similarity search.
- **Update**: Modify existing vectors.
- **Delete**: Remove vectors from the database.

You can find the code examples in the [\`chroma_db/\`](chroma_db/) directory.

## pgvector Examples

**pgvector** is an extension for PostgreSQL that adds support for vector data types. It allows you to store and query vectors in a relational database.

### CRUD Operations for pgvector

- **Create**: Insert vector data into a \`pgvector\` table.
- **Read**: Query vectors using Postgres SQL with similarity functions.
- **Update**: Modify vectors in a \`pgvector\` column.
- **Delete**: Remove vectors from the table.

Examples are located in the [\`pgvector/\`](pgvector/) directory.

## Usage

To run any of the examples:
1. Ensure the PostgreSQL and Chroma DB services are running.
2. Execute the Python scripts in either the \`chroma_db/\` or \`pgvector/\` folders to see CRUD operations in action.

Example command for running \`pgvector\` CRUD script:

\`\`\`bash
python pgvector/crud_example.py
\`\`\`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request if you'd like to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
