-- Setup to run on v0 data
BEGIN;
CREATE TEMP TABLE target_raw AS SELECT * FROM read_csv(
    ?, 
    union_by_name=true,
    filename=true
);

SELECT count(*) FROM target_raw as total_count_copied;

-- here is the list of columns that I'm referencing for normalizing/import
-- during ingest
-- select 
    -- "styles_ndsLink__GUaai",
    -- "styles_ndsTruncate__GRSDE", 
    -- "sc-f9ebbc4c-3",
    -- "sc-f9ebbc4c-3 (2)",
    -- "sc-f9ebbc4c-1", 
    -- "styles_ndsScreenReaderOnly__mcNC_" 
-- from target_bulk limit 10;

-- name: validate-target-input
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


COMMIT;