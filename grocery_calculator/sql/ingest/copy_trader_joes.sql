-- name: create-joes-extracted
CREATE TABLE IF NOT EXISTS trader_joes_extracted (
    product_label TEXT,
    primary_image TEXT,
    published INTEGER,
    sku TEXT,
    url_key TEXT,
    name TEXT,
    item_description TEXT,
    item_title TEXT,
    item_characteristics TEXT[], -- Array of strings
    sales_size DOUBLE,
    sales_uom_code TEXT,
    sales_uom_description TEXT,
    country_of_origin TEXT,
    availability TEXT,
    new_product TEXT,
    promotion TEXT,
    price_range_minimum_price_final_price_currency TEXT,
    price_range_minimum_price_final_price_value DOUBLE,
    price_range_minimum_price_final_price_type TEXT,
    price_range_minimum_price_min_price_type TEXT,
    price_range_price_range_type TEXT,
    retail_price TEXT,
    created_at TIMESTAMP,
    first_published_date TIMESTAMP,
    last_published_date TIMESTAMP,
    updated_at TIMESTAMP,
    items_type TEXT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- name: copy-trader-joes-files
INSERT INTO trader_joes_extracted (
    product_label,
    primary_image,
    published,
    sku,
    url_key,
    name,
    item_description,
    item_title,
    item_characteristics,
    sales_size,
    sales_uom_code,
    sales_uom_description,
    country_of_origin,
    availability,
    new_product,
    promotion,
    price_range_minimum_price_final_price_currency,
    price_range_minimum_price_final_price_value,
    price_range_minimum_price_final_price_type,
    price_range_minimum_price_min_price_type,
    price_range_price_range_type,
    retail_price,
    created_at,
    first_published_date,
    last_published_date,
    updated_at,
    items_type
)
WITH trader_joes_raw AS (
    SELECT * FROM read_json(
        ?,
        format = 'auto' 
    )
) 
SELECT 
    unnest(struct_extract(struct_extract(data, 'products'), 'items'), recursive := true)
FROM trader_joes_raw;

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
);

-- name: drop-null-rows
DROP FROM joes_ingest WHERE 
    sku IS NULL or
    retail_price IS NULL or
    item_title IS NULL or
    inserted_at IS NULL or
    store_code IS NULL or
    availability IS NULL or 
    product_detail IS NULL;

