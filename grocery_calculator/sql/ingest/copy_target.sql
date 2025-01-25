SET VARIABLE filepath = '/Users/jonjohnson/dev/bb-grocery-calculator/data/raw_input/target/v0/2025-01-23T16:02:54-08:00/*.csv';
SET VARIABLE trunc_file = SUBSTR(getvariable('filepath'), POSITION('v0' in getvariable('filepath')));
SET VARIABLE search_term = 'placeholder';

-- name: create-target-raw
-- Setup to run on v0 data
CREATE TEMP TABLE target_raw AS SELECT * FROM read_csv(
    getvariable('filepath'),
    union_by_name=true,
    filename=true
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
        "styles_ndsLink__GUaai" as brand,
        "styles_ndsTruncate__GRSDE" as product_name,
        "sc-f9ebbc4c-3" as price,
        "sc-f9ebbc4c-3 (2)" as orig_price,
        "sc-f9ebbc4c-1" as price_per,
        "styles_ndsScreenReaderOnly__mcNC_" as ratings
    FROM target_raw
    WHERE 1
        AND brand NOT NULL
        AND product_name NOT NULL
        AND price NOT NULL
        AND price_per NOT NULL;

-- name: count-rows-to-normalize
SELECT count(1) AS valid_rows FROM to_normalize;

