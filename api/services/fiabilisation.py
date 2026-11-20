"""Règles de fiabilisation des données (module métier testé).
"""
import pandas as pd
import datetime as dt

df_incidents = pd.read_csv("./data/incidents.csv")
df_stations = pd.read_csv("./data/stations.csv")
df_trajets = pd.read_csv("./data/trajets.csv")


def correction_doublons(df, df_nom):
    df_doublons=df[df.duplicated()] # donnees a supprimer
    df_clean=df[~(df.duplicated())] # donnees a garder
    lignes_invalides=[]
    for index, row in df_doublons.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "toutes",
            "valeur" : "/",
            "motif" : "lignes dupliquées",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def capacite_zero(df):
    df_incorrect=df[df["capacite"] <= 0] # donnees a supprimer
    df_clean=df[df["capacite"] > 0] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "stations.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "capacite",
            "valeur" : row["capacite"],
            "motif" : "capacité invalide : capacité inférieure à 1",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def format_date(df, df_nom, df_date, df_format):
    dates_propres = df.copy()

    date_iso = pd.to_datetime(
        dates_propres[df_date],
        format=df_format,
        errors="coerce",
    )

    date_fr = pd.to_datetime(
        dates_propres[df_date],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )

    dates_normalisees = date_iso.fillna(date_fr)

    dates_propres[df_date] = (
        dates_normalisees.dt.strftime(df_format)
    ) # donnees a garder

    df_clean = df.copy()
    df_clean[df_date] = pd.to_datetime(dates_propres[df_date]).dt.date

    df_incorrect = df[(df[df_date] != (df_clean[df_date])) & df[df_date].notna()]
    
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : df_date,
            "valeur" : row[df_date],
            "motif" : "date invalide : mauvais format de date",
            "décision" : "modification"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_dates(df):
    df_incorrect=df[(df["date_signalement"] >= df["date_resolution"]) & (df["date_resolution"].notna())] # donnees a supprimer
    df_clean=df[(df["date_signalement"] < df["date_resolution"]) | (df["date_resolution"].isna())] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "date_resolution",
            "valeur" : row["date_resolution"],
            "motif" : "durée invalide : date de résolution antérieure à date de signalement",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_cible(df):
    df_incorrect=df[
        (
            (df["cible"] == "velo")
            & ((df["velo_id"].isna()) 
            | (df["station_id"].notna()))
        ) 
        | 
        (
            (df["cible"] == "station")
            & ((df["velo_id"].notna()) 
            | (df["station_id"].isna()))
        )
    ] # donnees a supprimer
    df_clean=df[
        (
            (df["cible"] == "velo") 
            & (df["velo_id"].notna())
            & (df["station_id"].isna())
        ) 
        | 
        (
            (df["cible"] == "station")
            & (df["velo_id"].isna())
            & (df["station_id"].notna())
        )
    ] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "cible",
            "valeur" : row["cible"],
            "motif" : "durée invalide : incident ne correspond pas",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def id_existant(df, df_ref, id, id_ref, df_nom):
    df_incorrect=df[(~df[id].isin(df_ref[id_ref])) & df[id].notna()] # donnees a supprimer
    df_clean=df[df[id].isin(df_ref[id_ref]) | df[id].isna()] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : id,
            "valeur" : row[id],
            "motif" : "durée invalide : id non existant",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_usager(df):
    df_incorrect=df[
        (
            (df["type_usager"] == "occasionnel")
            & (df["usager_ref"].notna())
        ) 
        | 
        (
            (df["type_usager"] == "abonne")
            & (df["usager_ref"].isna())
        )
    ] # donnees a supprimer
    df_clean=df[
        (
            (df["type_usager"] == "occasionnel")
            & (df["usager_ref"].isna())
        ) 
        | 
        (
            (df["type_usager"] == "abonne")
            & (df["usager_ref"].notna())
        ) 
    ] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "trajets.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "usager_ref",
            "valeur" : row["usager_ref"],
            "motif" : "usager invalide : usager_ref n'est pas valide",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def technicien_manquant(df):
    df_incorrect=df[
        (
            (df["statut"].isin(["resolu", "en_cours"]))
            & df["technicien"].isna()
        )
    ]
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "technicien",
            "valeur" : row["technicien"],
            "motif" : "technicien invalide : technicien manquant après résolution",
            "décision" : "gardé"
        }
        lignes_invalides.append(ligne_invalide)
    return lignes_invalides


def station_manquante(df):
    df_incorrect=df[df["station_arrivee"].isna()]
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "trajets.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "station_arrivee",
            "valeur" : row["station_arrivee"],
            "motif" : "station d'arrivée invalide : station manquante",
            "décision" : "gardé"
        }
        lignes_invalides.append(ligne_invalide)
    return lignes_invalides

def format_statut(df):
    df_incorrect=df[~df["statut"].astype(str).str.islower()] # donnees a supprimer
    df_clean = df.copy()
    df_clean["statut"]=df["statut"].astype(str).str.lower() # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "statut",
            "valeur" : row["statut"],
            "motif" : "status invalide : mauvais format",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides