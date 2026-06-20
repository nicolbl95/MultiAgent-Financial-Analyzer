import os
import sys

# 1. Configurer la variable d'environnement Protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# 2. Configuration des chemins du package agents
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

sys.modules['agents'] = __import__('agents')

import streamlit as st
import tempfile
from graph_builder import AgentState, build_graph # Importation depuis graph_builder

# On initialise le graphe une seule fois au chargement global
graph = build_graph()

st.set_page_config(page_title="Analyseur Financier IA", page_icon="📊")
st.title("Assistant IA — Analyse Financière Multi-Agents")
st.write("Déposez un rapport financier PDF. 3 agents IA l'analysent en séquence.")

with st.sidebar:
    st.header("Architecture du système")
    st.write("1. Agent Extracteur (ChromaDB + RAG)")
    st.write("2. Agent Analyste (ChromaDB + Query)")
    st.write("3. Agent Rédacteur (LangGraph + Groq)")

def run_analysis(pdf_path: str):
    with st.status("Traitement du document par les agents IA...", expanded=True) as status:
        st.write("🕵️‍♂️ Étape 1 : L'Agent Extracteur récupère le texte du PDF...")
        st.write("🧠 Étape 2 : L'Agent Analyste évalue les risques financiers...")
        st.write("✍️ Étape 3 : L'Agent Rédacteur finalise la synthèse...")

        input_state: AgentState = {"pdf_path": pdf_path}
        result = graph.invoke(input_state)
        status.update(label="Analyse terminée avec succès !", state="complete", expanded=False)

    return result

uploaded_file = st.file_uploader("Choisir un PDF", type="pdf")

st.write("Ou bien sélectionnez un rapport PDF d'exemple pour lancer l'analyse immédiatement 🔽")

sample_dir = os.path.join(project_root, "sample_reports")

sample_files = {
    "BioSensus 2025": "Rapport_Performance_BioSensus_2025.pdf",
    "TechNova": "Rapport_Financier_TechNova.pdf",
    "OmniDrive": "Rapport_Financier_Avance_OmniDrive.pdf",
}

def resolve_sample_path(filename: str) -> str | None:
    # Priorité au dossier sample_reports dans le projet
    candidates = [
        os.path.join(sample_dir, filename),
        os.path.join(project_root, filename),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    # Recherche dans tout le projet pour gérer les déplacements internes
    for root, _, files in os.walk(project_root):
        if filename in files:
            return os.path.join(root, filename)

    return None

example_reports = {
    label: resolve_sample_path(filename)
    for label, filename in sample_files.items()
}

# Création des colonnes principales pour accueillir chaque exemple
cols = st.columns(len(example_reports))
selected_example = None
selected_example_label = None

for col, (label, path) in zip(cols, example_reports.items()):
    with col:
        # Création de sous-colonnes internes pour coller l'icône de téléchargement à droite du bouton
        sub_col1, sub_col2 = st.columns([3, 1])
        
        with sub_col1:
            if st.button(label, use_container_width=True):
                selected_example = path
                selected_example_label = label
                
        with sub_col2:
            # Si le fichier existe, on propose son téléchargement direct
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="📥",
                        data=f.read(),
                        file_name=os.path.basename(path),
                        mime="application/pdf",
                        key=f"dl_{label}" # Clé Streamlit unique par bouton
                    )
            else:
                st.caption("❌")

result = None

if selected_example_label is not None:
    if selected_example is None or not os.path.exists(selected_example):
        st.error(
            f"Fichier d'exemple introuvable pour '{selected_example_label}'. "
            "Vérifiez que les rapports PDF sont présents dans le projet."
        )
    else:
        result = run_analysis(selected_example)
elif uploaded_file and st.button("Lancer l'analyse IA"):
    # Création du fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    result = run_analysis(tmp_path)

    # Nettoyage du fichier temporaire après l'analyse
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

if result is not None:
    st.subheader("Analyse des risques")
    st.markdown(result.get("analysis", "Aucune analyse générée."))

    st.subheader("Synthèse pour dirigeants")
    st.markdown(result.get("summary", "Aucune synthèse générée."))