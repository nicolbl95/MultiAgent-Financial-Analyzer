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
import plotly.graph_objects as go
import plotly.express as px
from graph_builder import AgentState, build_graph # Importation depuis graph_builder

# On initialise le graphe une seule fois au chargement global
graph = build_graph()

# Configuration large pour que les graphiques aient de la place
st.set_page_config(page_title="Analyseur Financier IA", page_icon="📊", layout="wide")
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

# Fonctions d'affichages isolées des graphiques pour les injecter au bon endroit
def render_chart_1(report_label):
    if report_label == "OmniDrive":
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=['2024', '2025'], y=[48.12, 62.45], text=['48.12M€', '62.45M€'], textposition='auto', marker_color='#1f77b4'))
        fig1.update_layout(title="Focus : Croissance du Chiffre d'Affaires (M€)", template="plotly_dark", height=280)
        st.plotly_chart(fig1, use_container_width=True)
    elif report_label == "BioSensus 2025":
        fig1 = go.Figure(data=[
            go.Bar(name='Capitaux Propres', x=['BioSensus'], y=[31.2], marker_color='#2ca02c'),
            go.Bar(name='Dette Globale', x=['BioSensus'], y=[22.5], marker_color='#d62728')
        ])
        fig1.update_layout(barmode='group', title="Focus : Structure de Financement & Levée de fonds (M€)", template="plotly_dark", height=280)
        st.plotly_chart(fig1, use_container_width=True)
    elif report_label == "TechNova":
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=['2024', '2025', 'Prévisions 2026'], y=[59.3, 84.15, 120.0], mode='lines+markers', line=dict(color='#ff7f0e', width=3)))
        fig1.update_layout(title="Focus : Trajectoire de Croissance Initiale (M€)", template="plotly_dark", height=250)
        st.plotly_chart(fig1, use_container_width=True)

def render_chart_2(report_label):
    if report_label == "OmniDrive":
        labels = ['OmniCloud Brain AI (SaaS)', 'Intégration Matérielle / Usines']
        values = [28.90, 33.55]
        fig2 = px.pie(values=values, names=labels, title="Focus : Répartition des Flux de Revenus", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        fig2.update_layout(template="plotly_dark", height=280)
        st.plotly_chart(fig2, use_container_width=True)
    elif report_label == "BioSensus 2025":
        categories = ['Marge Brute', 'EBITDA Ajusté', 'Résultat Opérationnel (EBIT)']
        values = [32.02, 14.15, 8.92]
        fig2 = go.Figure([go.Bar(x=categories, y=values, marker_color=['#1f77b4', '#ff7f0e', '#9467bd'], text=[f"{v}M€" for v in values], textposition='auto')])
        fig2.update_layout(title="Focus : Soldes Intermédiaires de Gestion & Marges (M€)", template="plotly_dark", height=280)
        st.plotly_chart(fig2, use_container_width=True)
    elif report_label == "TechNova":
        fig2 = go.Figure(data=[go.Pie(labels=['Dette Bancaire LT', 'Avances Étatiques'], values=[22.0, 9.5], hole=0.3)])
        fig2.update_layout(title="Focus : Répartition de la Structure Endettement (M€)", template="plotly_dark", height=250)
        st.plotly_chart(fig2, use_container_width=True)

def render_chart_3(report_label):
    if report_label == "TechNova":
        fig3 = go.Figure([go.Bar(x=['Marge Brute', 'R&D', 'EBITDA'], y=[32.14, 18.5, 12.91], marker_color='#17becf')])
        fig3.update_layout(title="Focus : Performance Opérationnelle (M€)", template="plotly_dark", height=250)
        st.plotly_chart(fig3, use_container_width=True)


uploaded_file = st.file_uploader("Choisir un PDF", type="pdf")

st.write("Ou bien sélectionnez un rapport PDF d'exemple pour lancer l'analyse immédiatement 🔽")

sample_dir = os.path.join(project_root, "sample_reports")

sample_files = {
    "BioSensus 2025": "Rapport_Performance_BioSensus_2025.pdf",
    "TechNova": "Rapport_Financier_TechNova.pdf",
    "OmniDrive": "Rapport_Financier_Avance_OmniDrive.pdf",
}

def resolve_sample_path(filename: str) -> str | None:
    candidates = [
        os.path.join(sample_dir, filename),
        os.path.join(project_root, filename),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    for root, _, files in os.walk(project_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

example_reports = {
    label: resolve_sample_path(filename)
    for label, filename in sample_files.items()
}

cols = st.columns(len(example_reports))
selected_example = None
selected_example_label = st.session_state.get("active_label", None)

for col, (label, path) in zip(cols, example_reports.items()):
    with col:
        sub_col1, sub_col2 = st.columns([3, 1])
        with sub_col1:
            if st.button(label, use_container_width=True):
                selected_example = path
                selected_example_label = label
                st.session_state["active_label"] = label
                
        with sub_col2:
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="📥",
                        data=f.read(),
                        file_name=os.path.basename(path),
                        mime="application/pdf",
                        key=f"dl_{label}"
                    )
            else:
                st.caption("❌")

result = None

if selected_example_label is not None and selected_example is not None:
    if not os.path.exists(selected_example):
        st.error(f"Fichier d'exemple introuvable pour '{selected_example_label}'.")
    else:
        result = run_analysis(selected_example)
elif uploaded_file and st.button("Lancer l'analyse IA"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.session_state["active_label"] = "Custom Upload"
    result = run_analysis(tmp_path)

    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

if result is not None:
    active_report = st.session_state.get("active_label")

    # --- STRUCTURE DU RAPPORT FINANCIER IMBRIQUÉ ---
    st.markdown("---")
    
    # 1. Section Analyse Détaillée des Risques
    st.subheader("🕵️‍♂️ Rapport Spécifique d'Analyse des Risques")
    st.markdown(result.get("analysis", "Aucune analyse générée."))
    
    # Premier point d'insertion graphique juste après l'évaluation brute des risques
    st.markdown("### 📈 Visualisation Macro-Financière Associée")
    c1, c2 = st.columns(2)
    with c1:
        render_chart_1(active_report)
    with c2:
        render_chart_2(active_report)
        
    st.markdown("---")
    
    # 2. Section Synthèse Décisionnelle pour les Dirigeants
    st.subheader("✍️ Synthèse Exécutive pour le Comité de Direction")
    st.markdown(result.get("summary", "Aucune synthèse générée."))

    # Deuxième point d'insertion : Si c'est TechNova, on ajoute le 3ème graphique de performance tout à la fin
    if active_report == "TechNova":
        st.markdown("### 📊 Éléments Complémentaires de Performance Opérationnelle")
        render_chart_3(active_report)