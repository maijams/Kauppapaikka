CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE sale_items (
    id SERIAL PRIMARY KEY,
    header TEXT,
    content TEXT,
    category INTEGER,
    price INTEGER,
    user_id INTEGER REFERENCES users,
    location TEXT,
    sent_at TIMESTAMP,
    type INTEGER,
    visible BOOLEAN
);
CREATE TABLE user_favourites (
    user_id INTEGER REFERENCES users,
    sale_item_id INTEGER REFERENCES sale_items
);