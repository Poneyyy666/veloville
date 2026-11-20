# VéloVille — Plateforme de valorisation des données


VéloVille Hauts-de-France est un opérateur régional de vélos en libre-service. Ils possèdent actuellement dans la région 120 stations dans lesquelles sont répartis 1800 vélos. Environs 9000 trajets par jours sont recensés. 
Cette API a pour objectif de rendre la consultation des données propres de trajets et d'incidents de véloville accéccible rapidement ainsi que de 3 indicateurs des données. Elle permet aussi de modifier les status des incidents.S

Créez la base veloville et le rôle PostgreSQL associé, puis importez les données en lançant `importer.py`

Lancer l'api 

```bash
python -m uvicorn api.main:app --reload
```


Lancer streamlit

```bash
python -m streamlit run front/app.py
```


Lancer les tests

```bash
pytest --cov=api --cov-report=term-missing 
```

Coverage tests

| Name | Stmts | Miss | Cover | Missing |
|---|---|---|---|---|
| api\__init__.py | 0 | 0 | 100% | |
| api\config.py | 7 | 0 | 100% | |
| api\database.py | 12 | 4 | 67% | 33-37 |
| api\dependencies.py | 31 | 6 | 81% | 37-45, 52, 63 |
| api\main.py | 13 | 0 | 100% | |
| api\models.py | 42 | 0 | 100% | |
| api\routers\__init__.py | 0 | 0 | 100% | |
| api\routers\auth.py | 15 | 0 | 100% | |
| api\routers\incidents.py | 43 | 5 | 88% | 69-74 |
| api\routers\indicateurs.py | 23 | 0 | 100% | |
| api\routers\stations.py | 28 | 15 | 46% | 27-57, 72-84 |
| api\routers\trajets.py | 17 | 5 | 71% | 30-49 |
| api\schemas.py | 66 | 0 | 100% | |
| api\security.py | 17 | 3 | 82% | 19-27 |
| api\services\__init__.py | 0 | 0 | 100% | |
| api\services\fiabilisation.py | 90 | 0 | 100% | |
| api\services\indicateurs.py | 27 | 0 | 100% | |
| TOTAL | 431 | 38 | 91% | |