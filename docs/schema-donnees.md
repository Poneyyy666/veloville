# Schéma de données

À compléter : MLD textuel ou image, description des tables, clés et contraintes,
règles de gestion portées par le schéma.


## MLD

Stations = (station_id VARCHAR(4), nom VARCHAR(50), commune VARCHAR(50), capacite INT, latitude DECIMAL(15,5), longitude DECIMAL(15,5), date_mise_en_service DATE);

Trajets = (trajet_id VARCHAR(7), velo_id VARCHAR(5), depart_horodatage DATETIME, duree_secondes INT, type_usager VARCHAR(25), usager_ref VARCHAR(8), #station_id, #station_id_1*);

Incidents = (incident_id VARCHAR(10), date_signalement DATETIME, cible CHAR(10), velo_id VARCHAR(5), type_incident VARCHAR(25), statut VARCHAR(25), date_resolution DATE, technicien VARCHAR(50), #station_id*);
