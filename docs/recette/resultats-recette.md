# Résultats de recette

| Cas | Date et heure | Version testée (commit ou tag) | Statut | Preuve | Anomalie |
|---|---|---|---|---|---|
| REC-01 | 20/11/2026 | "Ajout des tests" | OK | Stations:120, Trajets:2011, Incidents:176 | |
| REC-02 | 20/11/2026 | "Ajout des tests" | OK | count_null:0 | |
| REC-03 | 20/11/2026 | "Ajout des tests" | OK | 200{"access_token": "token", "token_type": "bearer", "role": "exploitant"} 200{"access_token":"token", "token_type": "bearer", "role": "direction"}| |
| REC-04 | 20/11/2026 | "Ajout des tests" | OK | 401{"detail": "Identifiants invalides"} | |
| REC-05 | 20/11/2026 | "Ajout des tests" | OK | 401{"detail": "Authentification requise"} 200{"statut": "ok"} | |
| REC-06 | 20/11/2026 | "Ajout des tests" | OK | 403 {"detail": "Rôle non autorisé"} 200{"statut": "en cours"} 422{"Transition impossible : un incident 'en_cours' ne peut pas passer à 'en_cours'."} | |
| REC-07 | 20/11/2026 | "Ajout des tests" | OK | 200{"page": 1, "page_size": 50, "total": 120, "pages": 3} 200{"total": 46} For 'page_size': Value must be greater than or equal to 1. | |
| REC-08 | 20/11/2026 | "Ajout des tests" | OK | 200{"station_id": "S001", "nom": "Lille - Gare"} 404{"detail": "Station introuvable"} | |
| REC-09 | 20/11/2026 | "Ajout des tests" | OK | 200[{"depart_horodatage": "2026-08-24T00:00:00", "totalamount": 329}, {"depart_horodatage": "2026-08-28T00:00:00", "totalamount": 316}, {"depart_horodatage": "2026-08-25T00:00:00", "totalamount": 312}, {"depart_horodatage": "2026-08-26T00:00:00", "totalamount": 309}, {"depart_horodatage": "2026-08-27T00:00:00", "totalamount": 302}, {"depart_horodatage": "2026-08-30T00:00:00", "totalamount": 223}, {"depart_horodatage": "2026-08-29T00:00:00", "totalamount": 220}] | |
| REC-10 | 20/11/2026 | "Ajout des tests" | OK | empty, Ce site est inaccessible localhost n'autorise pas la connexion. | |

Synthèse : 10 cas exécutés sur 10 ; 10 OK, 0 KO, 0 NT ; 0 anomalies ouvertes, 0 corrigées.