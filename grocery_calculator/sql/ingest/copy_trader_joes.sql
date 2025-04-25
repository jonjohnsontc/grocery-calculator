-- name: copy-trader-joes-files
WITH trader_joes_raw AS (
    SELECT * FROM read_json(
        ?,
        format = 'array',
    )
), items AS (
    SELECT struct_extract(struct_extract(data, 'products'), 'items') as items
    FROM trader_joes_raw
) CREATE TABLE 
    trader_joes_extracted AS
    SELECT unnest(items) FROM items;


-- name: create-items-table
CREATE TABLE trader_joes_items AS
    SELECT struct_extract(struct_extract(data, 'products'), 'items') as items;

-- name: extract-items
CREATE TABLE trader_joes_extracted AS
    SELECT unnest(items) FROM trader_joes_items;



-- name: create-joes-ingest
CREATE TABLE IF NOT EXISTS joes_ingest (
    sku TEXT,
    retail_price TEXT,
    item_title TEXT,
    inserted_at TEXT,
    store_code TEXT,
    availability TEXT
    product_detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
)


COPY joes_ingest FROM ?;

DROP FROM joes_ingest WHERE 
    sku IS NULL or
    retail_price IS NULL or
    item_title IS NULL or
    inserted_at IS NULL or
    store_code IS NULL or
    availability IS NULL or 
    product_detail IS NULL;

