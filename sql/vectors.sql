-- Half-precision vectors

-- You can use the halfvec type to store half-precision vectors, as shown here:
CREATE TABLE items (
    id bigserial PRIMARY KEY,
    embedding halfvec(3)
);


-- Binary vectors
-- Use the bit type to store binary vector embeddings:
CREATE TABLE items (
    id bigserial PRIMARY KEY,
    embedding bit(3)
);

INSERT INTO items (embedding) VALUES ('000'), ('111');

-- Get the nearest neighbors by Hamming distance (added in 0.7.0)
SELECT * FROM items ORDER BY embedding <~> '101' LIMIT 5;

-- Binary quantization
-- Use expression indexing for binary quantization:
CREATE INDEX ON items USING hnsw (
    (binary_quantize(embedding)::bit(3)) bit_hamming_ops
);

-- Get the nearest neighbors by Hamming distance:
SELECT * FROM items ORDER BY binary_quantize(embedding)::bit(3) <~> binary_quantize('[1,-2,3]') LIMIT 5;

-- Re-rank by the original vectors for better recall:
SELECT * FROM (
    SELECT * FROM items ORDER BY binary_quantize(embedding)::bit(3) <~> binary_quantize('[1,-2,3]') LIMIT 20
) ORDER BY embedding <=> '[1,-2,3]' LIMIT 5;

-- Sparse vectors
-- Use the sparsevec type to store sparse vectors:
CREATE TABLE items (id bigserial PRIMARY KEY, embedding sparsevec(5));

-- Insert vectors
-- The format is {index1:value1,index2:value2}/dimensions and indices start at 1 like SQL arrays.
INSERT INTO items (embedding) VALUES ('{1:1,3:2,5:3}/5'), ('{1:4,3:5,5:6}/5');

-- Get the nearest neighbors by L2 distance:
SELECT * FROM items ORDER BY embedding <-> '{1:3,3:1,5:2}/5' LIMIT 5;
