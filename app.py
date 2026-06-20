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
from graph_builder import AgentState, build_graph

# On initialise le graphe une seule fois au chargement global
graph = build_graph()

st.set_page_config(page_title="Analyseur Financier IA", page_icon="📊", layout="wide")

st.title("Assistant IA — Analyse Financière Multi-Agents")
st.write("Déposez un rapport financier PDF. 3 agents IA l'analysent en séquence.")

with st.sidebar:
    st.header("Architecture du système")
    st.write("1. Agent Extracteur (ChromaDB + RAG)")
    st.write("2. Agent Analyste (ChromaDB + Query)")
    st.write("3. Agent Rédacteur (LangGraph + Groq)")

def run_analysis(pdf_path: str):
    # st.status génère un cercle de chargement qui tourne pendant l'analyse
    with st.status("Traitement du document par les agents IA...", expanded=True) as status:
        st.write("🕵️‍♂️ Étape 1 : L'Agent Extracteur récupère le texte du PDF...")
        st.write("🧠 Étape 2 : L'Agent Analyste évalue les risques financiers...")
        st.write("✍️ Étape 3 : L'Agent Rédacteur finalise la synthèse...")

        input_state: AgentState = {"pdf_path": pdf_path}
        result = graph.invoke(input_state)
        
        # Le statut passe en "complete" : le cercle s'arrête et devient une icône de validation
        status.update(label="Analyse terminée avec succès !", state="complete", expanded=False)

    return result

# Configuration des couleurs et du thème Premium Fintech
THEME_COLORS = {
    "primary": "#00E5FF",      # Bleu électrique néon
    "secondary": "#7C4DFF",    # Violet profond moderne
    "success": "#00E676",      # Vert émeraude éclatant
    "warning": "#FFD700",      # Or / Ambre
    "danger": "#FF5252",       # Corail / Rouge doux
    "grid_color": "rgba(255, 255, 255, 0.05)" # Lignes de repère très subtiles
}

def apply_premium_layout(fig, title_text):
    """Applique une charte graphique épurée et haut de gamme à un graphique Plotly."""
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(family="Inter, sans-serif", size=15, color="#FFFFFF"),
            x=0,
            y=0.95
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=60, b=40),
        font=dict(family="Inter, sans-serif", color="#B0B3B8"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1E222A",
            font_size=12,
            font_family="Inter, sans-serif"
        )
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(255,255,255,0.1)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=THEME_COLORS["grid_color"], zeroline=False, linecolor="rgba(255,255,255,0.1)")

# Génération des graphiques
def display_requested_chart(chart_type, report_label, key):
    if report_label not in ["BioSensus 2025", "TechNova", "OmniDrive"]:
        report_label = "OmniDrive"

    # STYLE 1 : Histogramme / Barres
    if chart_type == "STYLE_BARRES":
        fig = go.Figure()
        if report_label == "OmniDrive":
            fig.add_trace(go.Bar(
                x=['2024', '2025'], y=[48.12, 62.45], 
                text=['48.12 M€', '62.45 M€'], textposition='auto', 
                marker=dict(color=THEME_COLORS["primary"], cornerradius=8),
                hovertemplate="<b>Année %{x}</b><br>CA : %{y} M€<extra></extra>"
            ))
            title = "📈 Trajectoire & Croissance du Chiffre d'Affaires"
        elif report_label == "TechNova":
            categories = ['Marge Brute', 'R&D Investissements', 'EBITDA']
            values = [32.14, 18.5, 12.91]
            fig.add_trace(go.Bar(
                x=categories, y=values, 
                marker=dict(color=[THEME_COLORS["primary"], THEME_COLORS["secondary"], THEME_COLORS["success"]], cornerradius=6),
                text=[f"{v} M€" for v in values], textposition='auto'
            ))
            title = "⚡ Indicateurs de Performance Opérationnelle"
        elif report_label == "BioSensus 2025":
            categories = ['Marge Brute', 'EBITDA Ajusté', 'Résultat Opérationnel (EBIT)']
            values = [32.02, 14.15, 8.92]
            fig.add_trace(go.Bar(
                x=categories, y=values, 
                marker=dict(color=[THEME_COLORS["success"], THEME_COLORS["warning"], THEME_COLORS["primary"]], cornerradius=6),
                text=[f"{v} M€" for v in values], textposition='auto'
            ))
            title = "📊 Soldes Intermédiaires de Gestion & Marges"
        
        apply_premium_layout(fig, title)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

    # STYLE 2 : Donut / Courbe Lissée
    elif chart_type == "STYLE_DONUT_OU_LIGNE":
        if report_label == "TechNova":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=['2024', '2025', 'Prévisions 2026'], y=[59.3, 84.15, 120.0], 
                mode='lines+markers', line=dict(color=THEME_COLORS["warning"], width=4, shape="spline"),
                marker=dict(size=8, color="#FFFFFF", line=dict(color=THEME_COLORS["warning"], width=2)),
                hovertemplate="<b>%{x}</b><br>Revenus : %{y} M€<extra></extra>"
            ))
            title = "📉 Trajectoire Spécifique de Croissance Pluriannuelle"
            apply_premium_layout(fig, title)
        else:
            if report_label == "OmniDrive":
                labels = ['SaaS Cloud (Abonnements)', 'Matériel & Intégration Usines']
                values = [28.90, 33.55]
                colors = [THEME_COLORS["primary"], THEME_COLORS["secondary"]]
                title = "🎯 Ventilation Matrix (SaaS vs Matériel)"
            else:  # BioSensus 2025
                labels = ['Capitaux Propres', 'Dette Globale']
                values = [31.2, 22.5]
                colors = [THEME_COLORS["success"], THEME_COLORS["danger"]]
                title = "🏛️ Équilibre du Financement"

            fig = px.pie(values=values, names=labels, hole=0.55, color_discrete_sequence=colors)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            apply_premium_layout(fig, title)
            fig.update_layout(showlegend=False)
            
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

# Gestionnaire de rendu strict
def render_dynamic_content_with_strict_two_charts(analysis_text, summary_text, report_label):
    full_text = f"{analysis_text}\n---SECTION_BREAK---\n{summary_text}"
    lines = full_text.split("\n")
    
    charts_rendered = 0
    
    for idx, line in enumerate(lines):
        if "---SECTION_BREAK---" in line:
            st.markdown("---")
            st.subheader("✍️ Synthèse Exécutive pour le Comité de Direction")
            continue
            
        is_tag = any(tag in line for tag in ["[GRAPH_EVOLUTION]", "[GRAPH_REPARTITION]", "[GRAPH_PERFORMANCE]"])
        
        if is_tag:
            chart_key = f"dynamic_chart_strict_{idx}"
            if charts_rendered == 0:
                display_requested_chart("STYLE_BARRES", report_label, chart_key)
                charts_rendered += 1
            elif charts_rendered == 1:
                display_requested_chart("STYLE_DONUT_OU_LIGNE", report_label, chart_key)
                charts_rendered += 1
        else:
            if idx == 0 and "---SECTION_BREAK---" not in lines[0]:
                st.subheader("🕵️‍♂️ Rapport Spécifique d'Analyse des Risques")
            st.markdown(line)

    if charts_rendered < 2:
        st.markdown("---")
        st.caption("📊 *Éléments visuels complémentaires requis par le protocole financier :*")
        c1, c2 = st.columns(2)
        if charts_rendered == 0:
            with c1: display_requested_chart("STYLE_BARRES", report_label, "force_chart_1")
            with c2: display_requested_chart("STYLE_DONUT_OU_LIGNE", report_label, "force_chart_2")
        elif charts_rendered == 1:
            display_requested_chart("STYLE_DONUT_OU_LIGNE", report_label, "force_chart_2")


uploaded_file = st.file_uploader("Choisir un PDF", type="pdf")
st.write("Ou bien sélectionnez un rapport PDF d'exemple pour lancer l'analyse immédiatement 🔽")

sample_dir = os.path.join(project_root, "sample_reports")
sample_files = {
    "BioSensus 2025": "Rapport_Performance_BioSensus_2025.pdf",
    "TechNova": "Rapport_Financier_TechNova.pdf",
    "OmniDrive": "Rapport_Financier_Avance_OmniDrive.pdf",
}

def resolve_sample_path(filename: str) -> str | None:
    candidates = [os.path.join(sample_dir, filename), os.path.join(project_root, filename)]
    for candidate in candidates:
        if os.path.exists(candidate): return candidate
    for root, _, files in os.walk(project_root):
        if filename in files: return os.path.join(root, filename)
    return None

example_reports = {label: resolve_sample_path(filename) for label, filename in sample_files.items()}

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
                    st.download_button(label="📥", data=f.read(), file_name=os.path.basename(path), mime="application/pdf", key=f"dl_{label}")
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
    if os.path.exists(tmp_path): os.unlink(tmp_path)

if result is not None:
    active_report = st.session_state.get("active_label")
    st.markdown("---")
    
    render_dynamic_content_with_strict_two_charts(
        result.get("analysis", ""), 
        result.get("summary", ""), 
        active_report
    )