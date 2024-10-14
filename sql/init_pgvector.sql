-- Install the extension we just compiled

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS items (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(3)
);
