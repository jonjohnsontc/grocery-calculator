-- name: get-target-detail
SELECT t.id, t.product_detail 
FROM target_preprocess t
LEFT JOIN preprocess_tagged p
    ON t.id = p.ppid
WHERE p.ppid IS NULL;

--name: copy-tagged-data
INSERT INTO preprocess_tagged (
    ppid, 
    product_name,
    product_type,
    flavor_or_variant,
    size,
    packaging_type,
    sale,
    sale_value,
    tags
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);