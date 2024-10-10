-- Get the nearest neighbors to a vector

-- Supported distance functions are:
    -- <-> - L2 distance
    -- <#> - (negative) inner product
    -- <=> - cosine distance
    -- <+> - L1 distance (added in 0.7.0)
    -- <~> - Hamming distance (binary vectors, added in 0.7.0)
    -- <%> - Jaccard distance (binary vectors, added in 0.7.0)

-- Get the nearest neighbor to a vector by L2 distance
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

-- Get the nearest neighbor to a row by L2 distance:
SELECT * FROM items WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM items WHERE id = 1) LIMIT 5;

-- Get rows within a certain distance
SELECT * FROM items WHERE embedding <-> '[3,1,2]' < 5;



-- Distances

-- Get the distance
SELECT embedding <-> '[3,1,2]' AS distance FROM items;

-- For inner product, multiply by -1 (since <#> returns the negative inner product)
SELECT (embedding <#> '[3,1,2]') * -1 AS inner_product FROM items;

-- For cosine similarity, use 1 - cosine distance
SELECT 1 - (embedding <=> '[3,1,2]') AS cosine_similarity FROM items;



-- Aggregates

-- Average vectors
SELECT AVG(embedding) FROM items;

-- Average groups of vectors
-- ALTER TABLE IF EXISTS items ADD column category_id INTEGER NOT NULL DEFAULT 30;

SELECT category_id, AVG(embedding) FROM items GROUP BY category_id;
