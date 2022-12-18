CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    header TEXT,
    type TEXT,
    content TEXT,
    category INTEGER,
    price INTEGER,
    user_id INTEGER REFERENCES users,
    location TEXT,
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE user_favourites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    sale_item_id INTEGER REFERENCES items,
    visible BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY, 
    content TEXT, 
    item_id INTEGER REFERENCES items, 
    sender_id INTEGER REFERENCES users, 
    sent_at TIMESTAMP
);

CREATE TABLE photos (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    data BYTEA, 
    item_id INTEGER REFERENCES items
);
