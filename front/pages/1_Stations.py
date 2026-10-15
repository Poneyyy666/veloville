"""Écran Stations.

À compléter : tableau des stations filtrable par commune, pagination.
"""
import sys
import streamlit as st

sys.path.append('../veloville')
import front.api_client as api_client

if "page_items" not in st.session_state:
  st.session_state["page_items"] = 1

st.header("Stations")

col1, col2 = st.columns(2)

with col1:
    commune = st.selectbox(
        "Commune",
        ("Toutes", "Lille", "Roubaix", "Tourcoing", "Villeneuve d'Ascq", "Marcq-en-Baroeul", "Lambersart", "Wattrelos", "Croix", "Mons-en-Baroeul"),
    )

with col2:
    taille_page = st.selectbox(
        "Taille de page",
        (10, 20, 50),
    )


col1, col2 = st.columns(2)

with col1 :
    page = st.number_input("Page", min_value=1, step=1)


try:
    # page/page_size sont des paramètres d'URL de GET /items.
    donnees = api_client.obtenir(
        "/stations",
        params={"commune": commune, "page": page, "page_size": taille_page},
    )

    with col2:
        st.text(f"{donnees['total']} stations au total")
    
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(donnees["stations"], use_container_width=True)
    st.caption(f"Page {donnees['page']} / {donnees['pages']}")