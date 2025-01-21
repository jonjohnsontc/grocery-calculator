CREATE OR REPLACE SEQUENCE category_seq;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT DEFAULT nextval('category_seq') PRIMARY KEY,
    parent_id INT,
    name TEXT NOT NULL
);

CREATE OR REPLACE SEQUENCE item_seq;

CREATE TABLE IF NOT EXISTS products (
    item_id INT DEFAULT nextval('item_seq') PRIMARY KEY,
    category_id INT NOT NULL,
    name TEXT NOT NULL,
    size INT NOT NULL,
    unit TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE IF NOT EXISTS product_tags (
    item_id INT NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    PRIMARY KEY (item_id, tag)
);

CREATE OR REPLACE SEQUENCE store_seq;

CREATE TABLE IF NOT EXISTS stores (
    store_id INT DEFAULT nextval('store_seq') PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS store_locations (
    store_id INT NOT NULL,
    location_lat DECIMAL(9, 6) NOT NULL,
    location_long DECIMAL(9, 6) NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    PRIMARY KEY (store_id, location_lat, location_long)
);

CREATE TABLE IF NOT EXISTS store_selection (
    store_id INT NOT NULL,
    item_id INT NOT NULL,
    price DECIMAL(6, 2) NOT NULL,
    last_found DATE,
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    PRIMARY KEY (store_id, item_id)
);

CREATE TABLE IF NOT EXISTS coupons (
    item_id INT NOT NULL,
    value DECIMAL(6, 2) NOT NULL,
    store_id INT NOT NULL,
    expiration DATE,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    PRIMARY KEY (item_id, value, store_id, expiration)
);

CREATE TABLE IF NOT EXISTS store_coupon_policies (
    store_id INT NOT NULL,
    category TEXT NOT NULL,
    min_spend DECIMAL(6, 2),
    discount_type TEXT NOT NULL --still need to confirm what the values are here
);

CREATE TABLE IF NOT EXISTS price_history (
    store_id INT NOT NULL,
    item_id INT NOT NULL,
    updated_date DATE NOT NULL,
    price DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    PRIMARY KEY (store_id, item_id, updated_date, price)
);

CREATE TABLE IF NOT EXISTS ingest_meta (
    filename TEXT NOT NULL PRIMARY KEY,
    store_name TEXT NOT NULL,
    search_term TEXT NOT NULL,
    pull_timestamp TIMESTAMP NOT NULL,
    source_url TEXT NOT NULL,
    status TEXT NOT NULL
);