SELECT * FROM items WHERE category_id = 123 ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

-- Create an index on one or more of the WHERE columns for exact search"
CREATE INDEX ON items (category_id);

-- Create a partial index on the vector column for approximate search:
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) WHERE (category_id = 123);

-- Use partitioning for approximate search on many different values of the WHERE columns:
CREATE TABLE items (embedding vector(3), category_id int) PARTITION BY LIST(category_id);
