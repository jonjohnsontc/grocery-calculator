CREATE TEMP TABLE joes_ingest (
    sku TEXT,
    retail_price TEXT,
    item_title TEXT,
    inserted_at TEXT,
    store_code TEXT,
    availability TEXT
)
COPY joes_ingest FROM ?;

SELECT count(1) FROM joes_ingest as total_rows_ingested;

DROP FROM joes_ingest WHERE 
    sku IS NULL or
    retail_price IS NULL or
    item_title IS NULL or
    inserted_at IS NULL or
    store_code IS NULL or
    availability IS NULL;

SELECT count(1) FROM joes_ingest as count_after_dropping_null_rows;

