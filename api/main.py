"""Point d'entrée de l'API VéloVille (FastAPI).

À compléter : créer l'application, inclure les routeurs (auth, stations, trajets,
incidents, indicateurs) et exposer GET /sante -> {"statut": "ok"}.

Lancement : uvicorn api.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, stations, trajets, incidents, indicateurs

app = FastAPI(
    title="Data Catalogue & Quality API",
    description="TP final : JWT, rôles, PostgreSQL, CRUD et CORS.",
    version="1.0.0",
)

# Autorise explicitement le client navigateur de démonstration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],

    # Autorise l'utilisation de credentials si nécessaire.
    allow_credentials=True,

    # Toutes les méthodes sont autorisées pour la démonstration.
    allow_methods=["*"],

    # Autorise notamment l'en-tête Authorization.
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stations.router)
app.include_router(trajets.router)
app.include_router(incidents.router)
app.include_router(indicateurs.router)



@app.get("/sante", tags=["Accueil"])
def sante():
    """Confirme que l'API fonctionne."""

    return {
        "statut": "ok",
    }