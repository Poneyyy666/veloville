-- Schéma de la base veloville (PostgreSQL 14+).
-- À compléter en respectant le contrat du sujet (types, clés, contraintes).
-- Le script doit être rejouable : prévoir les DROP ... IF EXISTS ou
-- CREATE TABLE IF NOT EXISTS.

DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS trajets;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS utilisateur;

-- ---------------------------------------------------------------
-- 1. Table station
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stations(
    station_id VARCHAR(4) CHECK (station_id LIKE 'S%' AND station_id LIKE '%[0-9]'),
    nom VARCHAR(50) NOT NULL,
    commune VARCHAR(50) NOT NULL,
    capacite INT CHECK (capacite > 0) NOT NULL,
    latitude DECIMAL(15,5) NOT NULL,
    longitude DECIMAL(15,5) NOT NULL,
    date_mise_en_service DATE NOT NULL,
    PRIMARY KEY(station_id)
);

-- ---------------------------------------------------------------
-- 2. Table trajet
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS trajets(
    trajet_id VARCHAR(7) CHECK (trajet_id LIKE 'T%' AND trajet_id LIKE '%[0-9]'),
    velo_id VARCHAR(5) CHECK (velo_id LIKE 'V%' AND velo_id LIKE '%[0-9]') NOT NULL,
    depart_horodatage DATE NOT NULL,
    station_depart VARCHAR(4) NOT NULL,
    station_arrivee VARCHAR(4),
    duree_secondes INT,
    type_usager VARCHAR(25) CHECK (type_usager IN ('abonne', 'occasionnel')) NOT NULL,
    usager_ref VARCHAR(9) CHECK (usager_ref LIKE 'U%' AND usager_ref LIKE '%[^0-9A-F]'),
    PRIMARY KEY(trajet_id),
    FOREIGN KEY(station_depart) REFERENCES Stations(station_id),
    FOREIGN KEY(station_arrivee) REFERENCES Stations(station_id)
);

-- ---------------------------------------------------------------
-- 3. Table incident
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS incidents(
    incident_id VARCHAR(10) CHECK (incident_id LIKE 'I2026-%' AND incident_id LIKE '%[0-9]'),
    date_signalement DATE NOT NULL,
    cible CHAR(10) NOT NULL,
    velo_id VARCHAR(5) CHECK (velo_id LIKE 'V%' AND velo_id LIKE '%[0-9]'),
    station_id VARCHAR(4),
    type_incident VARCHAR(25) CHECK (type_incident IN ('vandalisme', 'selle abimee', 'eclairage HS', 'chaine deraillee', 'ecran borne illisible', 'pneu creve', 'frein defectueux', 'borne hors service')) NOT NULL,
    statut VARCHAR(25) CHECK (statut IN ('ouvert', 'en_cours', 'resolu')) NOT NULL,
    date_resolution DATE,
    technicien VARCHAR(50),
    PRIMARY KEY(incident_id),
    FOREIGN KEY(station_id) REFERENCES Stations(station_id)
);

-- ---------------------------------------------------------------
-- 4. Table utilisateur
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS utilisateur (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------------
-- 5. Index utiles aux filtres et aux indicateurs
-- ---------------------------------------------------------------

-- On appelle la commune pour filtrer les stations et le statut 
-- pour les incidents fréquement.

CREATE INDEX idx_commune
    ON Stations(commune);

CREATE INDEX idx_statut
    ON Incidents(statut);