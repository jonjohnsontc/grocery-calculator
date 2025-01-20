CREATE OR REPLACE SEQUENCE category_seq;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT DEFAULT nextval('category_seq') PRIMARY KEY,
    parent_id INT,
    name TEXT
);

CREATE OR REPLACE SEQUENCE item_seq;

CREATE TABLE IF NOT EXISTS products (
    item_id INT DEFAULT nextval('item_seq') PRIMARY KEY,
    category_id INT,
    name TEXT,
    size INT,
    unit TEXT,
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE IF NOT EXISTS product_tags (
    item_id INT,
    tag TEXT,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    PRIMARY KEY (item_id, tag)
);

CREATE OR REPLACE SEQUENCE store_seq;

CREATE TABLE IF NOT EXISTS stores (
    store_id INT DEFAULT nextval('store_seq') PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS store_locations (
    store_id INT,
    location_lat DECIMAL(9, 6),
    location_long DECIMAL(9, 6),
    FOREIGN KEY (store_id) REFERENCES store_id (store_id),
    PRIMARY KEY (store_id, location_lat, location_long)
);

CREATE TABLE IF NOT EXISTS coupons (
    item_id INT,
    value DECIMAL(6, 2),
    store_id INT,
    expiration DATE,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    PRIMARY KEY (item_id_id, value, store_id, expiration)
);