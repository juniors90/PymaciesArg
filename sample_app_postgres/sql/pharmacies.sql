CREATE TABLE IF NOT EXISTS pharmacies (
    id Integer PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    id_location Integer NOT NULL,
    id_department Integer NOT NULL,
    postal_code Integer NOT NULL, 
    adress VARCHAR(255) NOT NULL
);