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
    FOREIGN KEY (store_id) REFERENCES store_id (store_id),
    PRIMARY KEY (store_id, location_lat, location_long)
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

CREATE TABLE IF NOT EXISTS price_history (
    store_id INT NOT NULL,
    item_id INT NOT NULL,
    updated_date DATE NOT NULL,
    price DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES products (item_id),
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    PRIMARY KEY (store_id, item_id, updated_date, price)
)