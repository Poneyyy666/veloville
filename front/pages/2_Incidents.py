"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""
import sys
import streamlit as st

sys.path.append('../veloville')
import front.api_client as api_client

if "page_items" not in st.session_state:
  st.session_state["page_items"] = 1

st.header("Incidents")

col1, col2 = st.columns(2)

with col1:
    statut = st.selectbox(
        "Status",
        ("Tous", "ouvert", "en cours", "resolu"),
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
        "/incidents",
        params={"statut": statut, "page": page, "page_size": taille_page},
    )

    with col2:
        st.text(f"{donnees['total']} incidents au total")
    
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(donnees["incidents"], use_container_width=True)
    st.caption(f"Page {donnees['page']} / {donnees['pages']}")

with st.form("add_todo", clear_on_submit=True):
    id_incident = st.selectbox("Incident", api_client.appeler("GET", "/incidents/incidents_ids",), index=1)
    status = st.selectbox("Nouveau statut", ["en cours", "resolu"], index=1)
    submitted = st.form_submit_button("Appliquer")

    if submitted:
        payload = {
            "id_incident": id_incident,
            "status_incident": status,
        }
    
        try:
            nouvelle_todo = api_client.appeler(
                "PUT",
                "/incidents/update_dataset",
                params=payload,
            )
                
            st.success(f"Todo créée avec l'id {nouvelle_todo['id']}")
        except :
            pass