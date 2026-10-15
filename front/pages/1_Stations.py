"""Écran Stations.

À compléter : tableau des stations filtrable par commune, pagination.
"""
import streamlit as st

import api_client
import commun

st.header("3. Données publiques paginées")

try:
    # page/page_size sont des paramètres d'URL de GET /items.
    donnees = api_client.obtenir(
        "/stations",
        params={"page": st.session_state["page_items"], "page_size": 5},
    )
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(donnees["items"], use_container_width=True)
    st.caption(f"Page {donnees['page']} / {donnees['pages']} — {donnees['total']} éléments")

    precedent, suivant = st.columns(2)
    with precedent:
        if st.button("Précédent", disabled=donnees["page"] <= 1):
            st.session_state["page_items"] -= 1
            st.rerun()
    with suivant:
        if st.button("Suivant", disabled=donnees["page"] >= donnees["pages"]):
            st.session_state["page_items"] += 1
            st.rerun()