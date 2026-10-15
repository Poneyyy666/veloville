"""Page d'accueil Streamlit : connexion.

À compléter : formulaire identifiant / mot de passe, appel de POST /auth/login via
api_client, stockage du jeton et du rôle dans st.session_state,
message d'erreur en français en cas d'échec.

Lancement : streamlit run front/app.py
"""

import streamlit as st

import api_client
import commun

st.set_page_config(page_title="Démo 04 - FastAPI et Streamlit", layout="wide")
st.title("Démo 04 — Streamlit et FastAPI")

# Streamlit réexécute ce script après chaque interaction.
# st.session_state permet de conserver le numéro de page et le JWT.
if "page_items" not in st.session_state:
    st.session_state["page_items"] = 1

# ---- 1. Authentification JWT ----
st.header("1. Authentification")

if not commun.est_connecte():
    # st.form soumet les deux champs ensemble (pas à chaque caractère).
    with st.form("connexion"):
        identifiant = st.text_input("Identifiant")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        soumettre = st.form_submit_button("Se connecter")

    if soumettre:
        try:
            # L'appel HTTP est délégué au client API centralisé.
            reponse = api_client.connexion(identifiant, mot_de_passe)
        except api_client.ErreurApi as erreur:
            st.error(erreur.message)
        else:
            # JWT conservé uniquement pour la session Streamlit en cours.
            commun.connecter(identifiant, reponse)
            st.rerun()
else:
    st.success(f"Connecté en tant que {st.session_state['username']} (rôle : {st.session_state['role']}).")
    if st.button("Se déconnecter"):
        commun.deconnecter()
        st.rerun()