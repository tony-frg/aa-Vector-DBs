/*
An HNSW index creates a multilayer graph. It has better query performance than an
IVFFlat index (in terms of speed-recall tradeoff), but has slower build times and uses
more memory. Also, an HNSW index can be created without any data in the table since
there isn’t a training step like there is for an IVFFlat index.
*/
-- L2 distance:
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);

-- Inner product:
CREATE INDEX ON items USING hnsw (embedding vector_ip_ops);

-- Cosine distance:
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);

-- L1 distance:
CREATE INDEX ON items USING hnsw (embedding vector_l1_ops);

-- Hamming distance:
CREATE INDEX ON items USING hnsw (embedding bit_hamming_ops);

-- Jaccard distance:
CREATE INDEX ON items USING hnsw (embedding bit_jaccard_ops);


-- HNSW index build options
--    m - the max number of connections per layer (16 by default)
--    ef_construction - the size of the dynamic candidate list for constructing the graph (64 by default)
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) WITH (m = 16, ef_construction = 64);

-- HNSW index query options
SET hnsw.ef_search = 100;

-- use SET LOCAL inside a transaction to set ef_search for a single query:
BEGIN;
SET LOCAL hnsw.ef_search = 100;
SELECT * FROM items WHERE embedding <-> '[3,1,2]' < 5;
COMMIT;

-- HNSW index build time


-- Check indexing progress
-- The phases for HNSW are:
--     - initializing
--     - loading tuples
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
