-- Add a vector column to an existing table
ALTER TABLE items ADD COLUMN new_embedding_col vector(3);

-- Insert vectors
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');

-- Or load vectors in bulk using COPY
COPY items (embedding) FROM STDIN WITH (FORMAT BINARY);

-- Upsert vectors
INSERT INTO items (id, embedding) VALUES (1, '[1,2,3]'), (2, '[4,5,6]')
    ON CONFLICT (id) DO UPDATE SET embedding = EXCLUDED.embedding;

-- Update vectors
UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;

-- Delete vectors
DELETE FROM items WHERE id = 1;
