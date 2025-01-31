SET VARIABLE filepath = '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target/v0/2025-01-23T16:02:54-08:00/*.csv';
SET VARIABLE trunc_file = SUBSTR(getvariable('filepath'), POSITION('v0' in getvariable('filepath')));
SET VARIABLE search_term = 'placeholder';

-- name: create-target-raw
-- Setup to run on v0 data
CREATE TABLE target_raw AS SELECT * FROM read_csv(
    getvariable('filepath'),
    union_by_name=true,
    filename=true
);

COPY target_raw TO '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target_raw.csv' (
    HEADER, 
    DELIMITER ',', 
    RETURN_FILES
);

-- name: count-target-raw
SELECT count(*) as total_count_copied FROM target_raw;

-- name: validate-target-raw
-- validate that required columns exist after copying table
WITH required_columns AS (
    SELECT *
    FROM (
        VALUES 
        ('styles_ndsLink__GUaai'), 
        ('styles_ndsTruncate__GRSDE'), 
        ('sc-f9ebbc4c-3'),
        ('sc-f9ebbc4c-3 (2)'),
        ('sc-f9ebbc4c-1'),
        ('styles_ndsScreenReaderOnly__mcNC_')
        ) 
        AS t(column_name)
),
existing_columns AS (
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'target_raw'
)
SELECT CASE
           WHEN COUNT(*) = (SELECT COUNT(*) FROM required_columns) THEN 'All columns exist'
           ELSE 'Missing columns'
       END AS status
FROM required_columns
LEFT JOIN existing_columns USING (column_name);

-- name: check-for-file
-- check if the file exists
WITH file_check AS (
    SELECT COUNT(*) AS file_exists
    FROM ingest_meta
    WHERE filename = getvariable('trunc_file')
)
SELECT CASE
    WHEN file_exists = 0 THEN 'process_file'
    ELSE 'stop_pipeline'
END AS action
FROM file_check;

--name: add-file
INSERT INTO ingest_meta (filename, store_name, search_term, pull_timestamp, source_url, status)
    VALUES (
        getvariable('trunc_file'),
        'target',
        getvariable('search_term'),
        now(),
        'https://www.target.com/',
        'processing'
        );

-- name: create-to-normalize-table
CREATE TEMP TABLE to_normalize AS 
    SELECT
        "styles_ndsLink__GUaai" as brand_and_or_product,
        "styles_ndsTruncate__GRSDE" as product_detail,
        "styles_ndsTruncate__GRSDE (2)" as product_detail_2,
        "sc-f9ebbc4c-3" as price,
        "sc-f9ebbc4c-3 (2)" as orig_price,
        "sc-f9ebbc4c-1" as price_per,
        "styles_ndsScreenReaderOnly__mcNC_" as ratings
    FROM target_raw
    WHERE 1
        AND (brand_and_or_product NOT NULL OR product_detail NOT NULL OR product_detail_2 NOT NULL)
        AND price NOT NULL;

-- name: count-rows-to-normalize
SELECT count(1) AS valid_rows FROM to_normalize;

-- name: find-rows-that-didnt-make-it
COPY (
    SELECT
        "styles_ndsLink__GUaai" as brand_and_or_product,
        "styles_ndsTruncate__GRSDE" as product_detail,
        "styles_ndsTruncate__GRSDE (2)" as product_detail_2,
        "sc-f9ebbc4c-3" as price,
        "sc-f9ebbc4c-3 (2)" as orig_price,
        "sc-f9ebbc4c-1" as price_per,
        "styles_ndsScreenReaderOnly__mcNC_" as ratings
    FROM target_raw
    EXCEPT
    SELECT * FROM to_normalize
) TO '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target_filtered_out.csv' (
    HEADER, 
    DELIMITER ',', 
    RETURN_FILES
);

-- name: export-to-normalize
COPY to_normalize TO '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target_to_normalize.csv' (
    HEADER,
    DELIMITER ',',
    RETURN_FILES
);

CREATE TEMP TABLE distinct_to_normalize

-- name: count-distinct-rows
SELECT
    COUNT(1) as distinct_rows
FROM 
    (
        SELECT 
            brand_and_or_product,
            product_detail,
            product_detail_2,
            price,
            orig_price,
            price_per,
            ratings
        FROM to_normalize
        GROUP BY brand_and_or_product, product_detail, product_detail_2, price, orig_price, price_per, ratings
    );

-- name: create-normalized-tabe
CREATE TEMP TABLE normalized AS
    SELECT
        LOWER(brand_and_or_product) as brand_and_or_product,
        LOWER(product_detail) as product_detail,
        LOWER(product_detail_2) as product_detail_2,
        LOWER(price) as price,
        LOWER(orig_price) as orig_price,
        LOWER(price_per) as price_per,
        LOWER(ratings) as ratings
    FROM to_normalize
    WHERE 1
    AND NOT contains(price, '-');

-- name: copy-normalized
COPY normalized TO '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target_normalized.csv' (
    HEADER,
    DELIMITER ',',
    RETURN_FILES
);

CREATE SEQUENCE IF NOT EXISTS preprocess_seq;

-- name: create-preprocess-for-tagging
CREATE TABLE IF NOT EXISTS target_preprocess (
    id INTEGER DEFAULT nextval('preprocess_seq'),
    product_detail TEXT,
    price TEXT,
    orig_price TEXT,
    price_per TEXT
);

-- name: insert-into-preprocess
INSERT INTO target_preprocess (product_detail, price, orig_price, price_per)
    SELECT
        COALESCE(brand_and_or_product, '') || ' | ' || COALESCE(product_detail, '') || ' | ' || COALESCE(product_detail_2, '') 
            as product_detail,
        price,
        orig_price,
        price_per
    FROM normalized;

-- name: copy-preprocess-table
COPY target_preprocess TO '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target_preprocessed.csv' (
    HEADER,
    DELIMITER ',',
    RETURN_FILES
);

-- name: count-rows-copied  
SELECT COUNT(1) FROM target_preprocess as rows_copied;

-- name: create-preprocess-tagged
-- I'm still not entirely sure how I'm handling preprocessed items, whether 
-- they're all together, 
CREATE TABLE IF NOT EXISTS preprocess_tagged (
    ppid INTEGER,
    product_name TEXT,
    flavor_or_variant TEXT,
    size TEXT,
    packaging_type TEXT,
    sale BOOLEAN,
    sale_value DECIMAL,
    tags TEXT[] 
);