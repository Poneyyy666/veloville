"""Écran Indicateurs.

À compléter : trois st.metric et trois tableaux issus des trois endpoints
/indicateurs. Aucun graphique.
"""

import sys
import streamlit as st

sys.path.append('../veloville')
import front.api_client as api_client

if "page_items" not in st.session_state:
  st.session_state["page_items"] = 1

st.header("Incidents")

col1, col2, col3 = st.columns(3)

with col1:
    date_depart = st.date_input(
        "Période : du",
    )

with col2:
    date_arrivee = st.date_input(
        "au",
    )

with col3 :
    stations = st.number_input("Stations", min_value=1, max_value=50, value=10, step=1)


try:
    # page/page_size sont des paramètres d'URL de GET /items.
    donnees_period = api_client.obtenir(
        "/indicateurs/trajet_periode",
        params={"date_debut": date_depart, "date_fin": date_arrivee},
    )

    donnees_stations = api_client.obtenir(
        "/indicateurs/trajets_stations",
        params={"limit": stations},
    )
    
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(donnees_period, use_container_width=True)
    st.dataframe(donnees_stations, use_container_width=True)