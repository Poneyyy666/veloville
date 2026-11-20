# Procédure de déploiement

Créez la base veloville et le rôle PostgreSQL associé, puis importez les données en lançant `importer.py`

Lancer l'api 

```bash
python -m uvicorn api.main:app --reload
```


Lancer streamlit

```bash
python -m streamlit run front/app.py
```
