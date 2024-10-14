/*
An IVFFlat index divides vectors into lists and searches a subset of those lists that are
closest to the query vector. It has faster build times and uses less memory than HNSW,
but has lower query performance with respect to the speed-recall tradeoff.
*/

-- L2 distance:
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

-- Inner product:
CREATE INDEX ON items USING ivfflat (embedding vector_ip_ops) WITH (lists = 100);

-- Cosine distance:
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Hamming distance:
CREATE INDEX ON items USING ivfflat (embedding bit_hamming_ops) WITH (lists = 100);

-- Jaccard distance:
CREATE INDEX ON items USING hnsw (embedding bit_jaccard_ops);



-- IVFFlat query options
SET ivfflat.probes = 10;

-- use SET LOCAL inside a transaction to set the number of probes for a single query:
BEGIN;
SET LOCAL ivfflat.probes = 10;
SELECT * FROM items WHERE embedding <-> '[3,1,2]' < 5;
COMMIT;

-- HNSW index build time
SET maintenance_work_mem='10 GB';
SET max_parallel_maintenance_workers = 7


-- Check indexing progress
-- The phases for HNSW are:
--     - initializing
--     - loading tuples
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
