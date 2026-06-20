import os
# Cette ligne doit être la toute première du projet pour contourner le bug Python 3.14 / Protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import tempfile
from main import build_graph

# On initialise le graphe une seule fois au chargement global
graph = build_graph()

st.set_page_config(page_title="Analyseur Financier IA", page_icon="📊")
st.title("Assistant IA — Analyse Financière Multi-Agents")
st.write("Déposez un rapport financier PDF. 3 agents IA l'analysent en séquence.")

with st.sidebar:
    st.header("Architecture du système")
    st.write("1. Agent Extracteur (ChromaDB + RAG)")
    st.write("2. Agent Analyste (Ollama / Llama 3)")
    st.write("3. Agent Rédacteur (LangGraph)")

uploaded_file = st.file_uploader("Choisir un PDF", type="pdf")

if uploaded_file and st.button("Lancer l'analyse IA"):
    # 1. Création du fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # 2. Lancement de la boîte de statut et exécution des agents
    with st.status("Traitement du document par les agents IA...", expanded=True) as status:
        st.write("🕵️‍♂️ Étape 1 : L'Agent Extracteur récupère le texte du PDF...")
        # (Le code de ton graphe s'exécute...)
        
        st.write("🧠 Étape 2 : L'Agent Analyste évalue les risques financiers...")
        # (L'analyse s'exécute...)
        
        st.write("✍️ Étape 3 : L'Agent Rédacteur finalise la synthèse...")
        # Appel du graphe (désormais tmp_path est bien accessible ici)
        result = graph.invoke({"pdf_path": tmp_path})
        
        # Quand c'est fini, on coche la boîte en vert !
        status.update(label="Analyse terminée avec succès !", state="complete", expanded=False)

    # 3. Nettoyage du fichier temporaire après l'analyse
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

    # 4. Affichage des résultats générés par les agents
    st.subheader("Analyse des risques")
    st.write(result.get("analysis", "Aucune analyse générée."))
    
    st.subheader("Synthèse pour dirigeants")
    st.write(result.get("summary", "Aucune synthèse générée."))