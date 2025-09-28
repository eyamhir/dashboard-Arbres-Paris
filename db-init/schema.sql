CREATE TABLE IF NOT EXISTS arbres_remarquables (
    id SERIAL PRIMARY KEY,
    genre TEXT,
    espece TEXT,
    adresse TEXT,
    arrondissement TEXT,
    date_plantation DATE,
    geo_lat DOUBLE PRECISION,
    geo_lon DOUBLE PRECISION
);
