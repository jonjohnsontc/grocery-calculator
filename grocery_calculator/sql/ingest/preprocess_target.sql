-- name: get-target-detail
SELECT id, product_detail FROM target_preprocess;

--name: copy-tagged-data
INSERT INTO preprocess_tagged (
    ppid, 
    product_name,
    flavor_or_variant,
    size,
    packaging_type,
    sale,
    sale_value,
    tags
) VALUES (?, ?, ?, ?, ?, ?, ?, ?);