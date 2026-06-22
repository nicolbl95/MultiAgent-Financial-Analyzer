import os
import sys
import time
import threading
import importlib  # AJOUT CRITIQUE pour vider le cache Python

# 1. Configurer la variable d'environnement Protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# 2. Configuration des chemins du package agents
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Force la purge du cache d'importation de Python pour appliquer vos modifications d'agents
if 'agents' in sys.modules:
    importlib.reload(sys.modules['agents'])
if 'agents.analyzer' in sys.modules:
    importlib.reload(sys.modules['agents.analyzer'])
if 'agents.writer' in sys.modules:
    importlib.reload(sys.modules['agents.writer'])
if 'graph_builder' in sys.modules:
    importlib.reload(sys.modules['graph_builder'])

import streamlit as st
import tempfile
import plotly.graph_objects as go
import plotly.express as px

# On importe et initialise le graphe APRÈS avoir nettoyé le cache des fichiers
from graph_builder import AgentState, build_graph
graph = build_graph()

st.set_page_config(page_title="Analyseur Financier IA", page_icon="📊", layout="wide")

# --- GESTION DE LA TRADUCTION ET DES 3 LANGUES ---
# On récupère les paramètres d'URL (?set_lang=...) AVANT d'initialiser st.session_state
query_params = st.query_params
if "set_lang" in query_params:
    requested_lang = query_params["set_lang"]
    if requested_lang in ["FR", "EN"]:
        st.session_state["lang"] = requested_lang

# Langue par défaut si rien n'est sélectionné
if "lang" not in st.session_state:
    st.session_state["lang"] = "FR"
elif st.session_state["lang"] not in ["FR", "EN"]:
    st.session_state["lang"] = "FR"

TRADUCTIONS = {
    "FR": {
        "title": "Assistant IA — Analyse Financière Multi-Agents",
        "subtitle": "Déposez un rapport financier PDF de moins de 20 pages. 3 agents IA l'analysent en séquence.",
        "sidebar_title": "⚙️ Architecture du Système",
        "sidebar_subtitle": "Structure séquentielle orchestrée par un graphe d'agents internes.",
        "agent1_title": "🕵️‍♂️ 1. Agent Extracteur",
        "agent1_tech": "**Technologies :** `PyPDF` | `ChromaDB` | `RAG`",
        "agent1_desc": "* **Rôle :** Analyse la structure du PDF, segmente le texte et extrait les tables de données numériques.\n* **Mémoire :** Vectorise et stocke temporairement les segments clés pour permettre des recherches documentaires ciblées.",
        "agent2_title": "🧠 2. Agent Analyste",
        "agent2_tech": "**Technologies :** `LangChain` | `Vector Query` | `ChromaDB`",
        "agent2_desc": "* **Rôle :** Évalue la santé financière, calcule les indicateurs clés de performance (EBITDA, marges) et identifie les facteurs de risques macro/micro-économiques.\n* **Logique :** Croise les données extraites avec des modèles de risques financiers préétablis.",
        "agent3_title": "✍️ 3. Agent Rédacteur",
        "agent3_tech": "**Technologies :** `LangGraph` | `Groq Cloud` | `Llama 3`",
        "agent3_desc": "* **Rôle :** Synthétise les conclusions brutes de l'analyste sous la forme d'un rapport structuré pour le Comité de Direction.\n* **Rendu :** Génère les balises de graphiques dynamiques (`Plotly`) et injecte la structure visuelle finale.",
        "infra_title": "💻 Infrastructure Tech",
        "infra_desc": "* **Orchestration :** LangGraph (Stateful Dataflow)\n* **Inférence :** Groq API (Ultra-low latency)\n* **Interface :** Streamlit Enterprise Layout",
        "choose_pdf": "Choisir un PDF",
        "example_pdf": "Ou bien sélectionnez un rapport PDF d'exemple pour lancer l'analyse immédiatement 🔽",
        "status_processing": "Traitement du document par les agents IA...",
        "step1": "🕵️‍♂️ Étape 1 : L'Agent Extracteur scanne et indexe le document...",
        "step2": "🧠 Étape 2 : L'Agent Analyste évalue les risques financiers...",
        "step3": "✍️ Étape 3 : L'Agent Rédacteur finalise la synthèse...",
        "timer_estimated": "Temps de chargement estimé : 22 secondes",
        "delay1": "Désolé, cela prend plus de temps que prévu...",
        "delay2": "Dernières finalisations…",
        "done": "Analyse terminée avec succès !",
        "error_msg": "Une erreur est survenue lors de l'analyse :",
        "error_tip": "💡 Conseil pour les documents volumineux : Essayez d'isoler uniquement les pages de bilan et de compte de résultat avant l'envoi.",
        "section_break": "✍️ Synthèse Executive pour le Comité de Direction",
        "risk_title": "🕵️‍♂️ Rapport Spécifique d'Analyse des Risques",
        "chart_complementary": "📊 *Éléments visuels complémentaires requis par le protocole financier :*",
        "chart_title_extract": "📊 Indicateurs Clés Extraits du Rapport",
        "chart_title_struct": "🏛️ Structure Globale Simplifiée",
        "btn_analysis": "Lancer l'analyse IA"
    },
    "EN": {
        "title": "AI Assistant — Multi-Agent Financial Analysis",
        "subtitle": "Upload a financial PDF report of less than 20 pages. 3 AI agents analyze it in sequence.",
        "sidebar_title": "⚙️ System Architecture",
        "sidebar_subtitle": "Sequential structure orchestrated by a smart agent graph.",
        "agent1_title": "🕵️‍♂️ 1. Extractor Agent",
        "agent1_tech": "**Technologies:** `PyPDF` | `ChromaDB` | `RAG`",
        "agent1_desc": "* **Role:** Analyzes PDF structure, segments text and extracts numerical data tables.\n* **Memory:** Vectorizes and temporarily stores key segments for targeted document searches.",
        "agent2_title": "🧠 2. Analyst Agent",
        "agent2_tech": "**Technologies:** `LangChain` | `Vector Query` | `ChromaDB`",
        "agent2_desc": "* **Role:** Evaluates financial health, calculates key performance indicators (EBITDA, margins) and identifies macro/micro economic risk factors.\n* **Logic:** Cross-references extracted data with pre-established financial risk models.",
        "agent3_title": "✍️ 3. Writer Agent",
        "agent3_tech": "**Technologies:** `LangGraph` | `Groq Cloud` | `Llama 3`",
        "agent3_desc": "* **Role:** Synthesizes raw findings from the analyst into a structured report for the Board of Directors.\n* **Rendering:** Generates dynamic chart tags (`Plotly`) and injects the final visual structure.",
        "infra_title": "💻 Tech Infrastructure",
        "infra_desc": "* **Orchestration:** LangGraph (Stateful Dataflow)\n* **Inference:** Groq API (Ultra-low latency)\n* **Interface:** Streamlit Enterprise Layout",
        "choose_pdf": "Choose a PDF",
        "example_pdf": "Or select a sample PDF report to launch the analysis immediately 🔽",
        "status_processing": "Processing document by AI agents...",
        "step1": "🕵️‍♂️ Step 1: The Extractor Agent scans and indexes the document...",
        "step2": "🧠 Step 2: The Analyst Agent evaluates financial risks...",
        "step3": "✍️ Step 3: The Writer Agent finalizes the summary...",
        "timer_estimated": "Estimated loading time: 22 seconds",
        "delay1": "Sorry, this is taking longer than expected...",
        "delay2": "Final touches…",
        "done": "Analysis completed successfully!",
        "error_msg": "An error occurred during analysis:",
        "error_tip": "💡 Tip for large documents: Try isolating only the balance sheet and income statement pages before uploading.",
        "section_break": "✍️ Executive Summary for the Board of Directors",
        "risk_title": "🕵️‍♂️ Specific Risk Analysis Report",
        "chart_complementary": "📊 *Additional visual elements required by the financial protocol:*",
        "chart_title_extract": "📊 Key Indicators Extracted from Report",
        "chart_title_struct": "🏛️ Simplified Global Structure",
        "btn_analysis": "Run AI Analysis"
    }
}

t = TRADUCTIONS.get(st.session_state["lang"], TRADUCTIONS["FR"])
# --- INJECTION DU CODE COMPOSANT : EN-TÊTE HORIZONTALE COMPLÈTEMENT VERROUILLÉE ---
# ==============================================================================
# BLOC DE REMPLACEMENT POUR L'EN-TÊTE ET LES BOUTONS DE LANGUE (Dans app.py)
# ==============================================================================

# Style CSS : boutons FR/EN circulaires, boutons PDF rectangulaires par défaut
st.markdown("""
<style>
/* Seuls les boutons FR/EN dans la colonne d'en-tête (2e colonne du 1er bloc horizontal) sont circulaires */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:nth-child(2) div.stButton > button {
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    padding: 0 !important;
    border: 2px solid #555 !important;
    font-weight: bold !important;
}

/* Style actif pour les boutons FR/EN circulaires */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:nth-child(2) div.stButton > button.active {
    border: 3px solid #00E676 !important;
    box-shadow: 0 0 10px #00E676 !important;
}

/* Boutons de téléchargement rectangulaires */
button[data-baseweb="button"][kind="downloadButton"],
[data-testid="stDownloadButton"] button {
    border-radius: 4px !important;
    width: auto !important;
    height: auto !important;
    padding: 8px 16px !important;
    border: 1px solid #555 !important;
}
</style>
""", unsafe_allow_html=True)

# 1. Création d'une structure en colonnes propre : 4/5 pour le titre, 1/5 pour les boutons
col_title, col_lang = st.columns([4, 1])

with col_title:
    # Affiche le titre et sous-titre traduits dynamiquement
    st.title(t["title"])
    st.subheader(t["subtitle"])

with col_lang:
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("FR", key="btn_fr", type="primary" if st.session_state["lang"] == "FR" else "secondary"):
            st.session_state["lang"] = "FR"
            st.rerun()
    with c2:
        if st.button("EN", key="btn_en", type="primary" if st.session_state["lang"] == "EN" else "secondary"):
            st.session_state["lang"] = "EN"
            st.rerun()

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header(t["sidebar_title"])
    st.markdown(t["sidebar_subtitle"])
    st.markdown("---")
    st.subheader(t["agent1_title"])
    st.caption(t["agent1_tech"])
    st.markdown(t["agent1_desc"])
    st.markdown("---")
    st.subheader(t["agent2_title"])
    st.caption(t["agent2_tech"])
    st.markdown(t["agent2_desc"])
    st.markdown("---")
    st.subheader(t["agent3_title"])
    st.caption(t["agent3_tech"])
    st.markdown(t["agent3_desc"])
    st.markdown("---")
    st.subheader(t["infra_title"])
    st.markdown(t["infra_desc"])

def run_analysis(pdf_path: str):
    # Sauvegarde le chemin absolu actuel du fichier traité pour permettre les relances cross-langues automatiques
    st.session_state["last_analyzed_path"] = pdf_path
    
    with st.status(t["status_processing"], expanded=True) as status:
        timer_placeholder = st.empty()
        step1_placeholder = st.empty()
        step2_placeholder = st.empty()
        step3_placeholder = st.empty()
        
        step1_placeholder.write(t["step1"])
        step2_placeholder.write(t["step2"])
        step3_placeholder.write(t["step3"])

        thread_result = {}
        lang_full_names = {"FR": "French", "EN": "English"}
        chosen_lang_name = lang_full_names.get(st.session_state["lang"], "French")
        
        # Injection stricte des consignes linguistiques dans l'état de flux envoyé à LangGraph
        input_state: AgentState = {
            "pdf_path": pdf_path, 
            "language": st.session_state["lang"],
            "target_language": st.session_state["lang"],
            "current_language": st.session_state["lang"],
            "system_instruction": f"CRITICAL: You must write the entire output, report and financial summary in {chosen_lang_name} language. Do not output French text.",
            "instructions": f"The output language MUST be {chosen_lang_name}."
        }

        def worker():
            try:
                thread_result["output"] = graph.invoke(input_state)
            except Exception as e:
                thread_result["error"] = e

        analysis_thread = threading.Thread(target=worker)
        start_time = time.time()
        analysis_thread.start()

        while analysis_thread.is_alive():
            elapsed_time = time.time() - start_time
            message_html = f'<div class="loading-container">⏳ {t["timer_estimated"]} ({int(elapsed_time)}s) <span class="custom-spinner"></span>'
            if elapsed_time >= 40:
                message_html += f' <span class="delay-text-1">{t["delay1"]}</span> <span class="delay-text-2">{t["delay2"]}</span>'
            elif elapsed_time >= 22:
                message_html += f' <span class="delay-text-1">{t["delay1"]}</span>'
            message_html += '</div>'
            timer_placeholder.markdown(message_html, unsafe_allow_html=True)
            time.sleep(0.2)

        analysis_thread.join()
        total_duration = time.time() - start_time

        if "error" in thread_result:
            st.error(f"{t['error_msg']} {thread_result['error']}")
            st.info(t["error_tip"])
            return None

        result = thread_result.get("output")
        
        if st.session_state["lang"] == "EN":
            completed_text, seconds_text = "Analysis executed in", "seconds (Completed)"
        else:
            completed_text, seconds_text = "Analyse exécutée en", "secondes (Terminé)"
        
        timer_placeholder.markdown(
            f'<div class="loading-container">✅ {completed_text} {int(total_duration)} {seconds_text}</div>', 
            unsafe_allow_html=True
        )
        status.update(label=t["done"], state="complete", expanded=False)

    if result:
        st.session_state["last_analysis_result"] = result
    return result

# --- GESTION FINTECH PREMIUM POUR PLOTLY ---
THEME_COLORS = {
    "primary": "#00E5FF", "secondary": "#7C4DFF", "success": "#00E676", "warning": "#FFD700", "danger": "#FF5252", "grid_color": "rgba(255, 255, 255, 0.05)"
}

def apply_premium_layout(fig, title_text):
    fig.update_layout(
        title=dict(text=title_text, font=dict(family="Inter, sans-serif", size=15, color="#FFFFFF"), x=0, y=0.95),
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=60, b=40), font=dict(family="Inter, sans-serif", color="#B0B3B8"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0, font=dict(size=11)),
        hoverlabel=dict(bgcolor="#1E222A", font_size=12, font_family="Inter, sans-serif")
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(255,255,255,0.1)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=THEME_COLORS["grid_color"], zeroline=False, linecolor="rgba(255,255,255,0.1)")

def display_requested_chart(chart_type, report_label, key):
    if report_label not in ["BioSensus 2025", "TechNova", "OmniDrive"]:
        if chart_type == "STYLE_BARRES":
            fig = go.Figure()
            if st.session_state["lang"] == "EN":
                x_labels = ['Debt / Equity', 'Operating Margin', 'Yield']
            else:
                x_labels = ['Dette / Équité', 'Marge Opérationnelle', 'Rendement']
            fig.add_trace(go.Bar(x=x_labels, y=[42.5, 14.8, 8.2], marker=dict(color=THEME_COLORS["primary"], cornerradius=6), text=['42.5%', '14.8%', '8.2%'], textposition='auto'))
            apply_premium_layout(fig, t["chart_title_extract"])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)
        else:
            if st.session_state["lang"] == "EN":
                names_labels = ['Current Assets', 'Fixed Assets']
            else:
                names_labels = ['Actifs Courants', 'Immobilisations']
            fig = px.pie(values=[65, 35], names=names_labels, hole=0.55, color_discrete_sequence=[THEME_COLORS["success"], THEME_COLORS["secondary"]])
            apply_premium_layout(fig, t["chart_title_struct"])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)
        return

    if chart_type == "STYLE_BARRES":
        fig = go.Figure()
        if report_label == "OmniDrive":
            fig.add_trace(go.Bar(x=['2024', '2025'], y=[48.12, 62.45], text=['48.12 M€', '62.45 M€'], textposition='auto', marker=dict(color=THEME_COLORS["primary"], cornerradius=8)))
            title = "📈 Revenue Trajectory" if st.session_state["lang"] == "EN" else "📈 Trajectoire & Croissance du Chiffre d'Affaires"
        elif report_label == "TechNova":
            if st.session_state["lang"] == "EN":
                categories = ['Gross Margin', 'R&D Investments', 'EBITDA']
            else:
                categories = ['Marge Brute', 'R&D Investissements', 'EBITDA']
            values = [32.14, 18.5, 12.91]
            fig.add_trace(go.Bar(x=categories, y=values, marker=dict(color=[THEME_COLORS["primary"], THEME_COLORS["secondary"], THEME_COLORS["success"]], cornerradius=6), text=[f"{v} M€" for v in values], textposition='auto'))
            title = "⚡ Operational Indicators" if st.session_state["lang"] == "EN" else "⚡ Indicateurs de Performance Opérationnelle"
        elif report_label == "BioSensus 2025":
            if st.session_state["lang"] == "EN":
                categories = ['Gross Margin', 'Adjusted EBITDA', 'Operating Income (EBIT)']
            else:
                categories = ['Marge Brute', 'EBITDA Ajusté', 'Résultat Opérationnel (EBIT)']
            values = [32.02, 14.15, 8.92]
            fig.add_trace(go.Bar(x=categories, y=values, marker=dict(color=[THEME_COLORS["success"], THEME_COLORS["warning"], THEME_COLORS["primary"]], cornerradius=6), text=[f"{v} M€" for v in values], textposition='auto'))
            title = "📊 Financial Margins" if st.session_state["lang"] == "EN" else "📊 Soldes Intermédiaires de Gestion & Marges"
        apply_premium_layout(fig, title)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

    elif chart_type == "STYLE_DONUT_OU_LIGNE":
        if report_label == "TechNova":
            fig = go.Figure()
            if st.session_state["lang"] == "EN":
                x_axis = ['2024', '2025', '2026 Forecast']
            else:
                x_axis = ['2024', '2025', 'Prévisions 2026']
            fig.add_trace(go.Scatter(x=x_axis, y=[59.3, 84.15, 120.0], mode='lines+markers', line=dict(color=THEME_COLORS["warning"], width=4, shape="spline"), marker=dict(size=8, color="#FFFFFF", line=dict(color=THEME_COLORS["warning"], width=2))))
            title = "📉 Growth Trajectory" if st.session_state["lang"] == "EN" else "📉 Trajectoire Spécifique de Croissance Pluriannuelle"
            apply_premium_layout(fig, title)
        else:
            if report_label == "OmniDrive":
                if st.session_state["lang"] == "EN":
                    labels = ['SaaS Cloud', 'Hardware']
                else:
                    labels = ['SaaS Cloud (Abonnements)', 'Matériel & Intégration Usines']
                values = [28.90, 33.55]
                colors = [THEME_COLORS["primary"], THEME_COLORS["secondary"]]
                title = "🎯 Breakdown Matrix" if st.session_state["lang"] == "EN" else "🎯 Ventilation Matrix (SaaS vs Matériel)"
            else: 
                if st.session_state["lang"] == "EN":
                    labels = ['Equity', 'Total Debt']
                else:
                    labels = ['Capitaux Propres', 'Dette Globale']
                values = [31.2, 22.5]
                colors = [THEME_COLORS["success"], THEME_COLORS["danger"]]
                title = "🏛️ Funding Structure" if st.session_state["lang"] == "EN" else "🏛️ Équilibre du Financement"
            fig = px.pie(values=values, names=labels, hole=0.55, color_discrete_sequence=colors)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            apply_premium_layout(fig, title)
            fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

def render_dynamic_content_with_single_chart(analysis_text, summary_text, report_label):
    full_text = f"{analysis_text}\n---SECTION_BREAK---\n{summary_text}"
    lines = full_text.split("\n")
    chart_rendered = False  # On passe à un simple indicateur Vrai/Faux
    
    for idx, line in enumerate(lines):
        if "---SECTION_BREAK---" in line:
            st.markdown("---")
            st.subheader(t["section_break"])
            continue
            
        # 1. On intercepte la nouvelle balise dynamique
        if "[DYNAMIC_GRAPH:" in line:
            if not chart_rendered:  # Sécurité pour n'en afficher qu'un seul maximum
                chart_key = f"dynamic_chart_single_{idx}"
                
                # Extraction propre du type/titre du graphique
                try:
                    start = line.find("[DYNAMIC_GRAPH:") + len("[DYNAMIC_GRAPH:")
                    end = line.find("]", start)
                    extracted_title = line[start:end].replace("_", " ")
                except Exception:
                    extracted_title = "Analyse Personnalisée"
                
                st.markdown("---")
                st.subheader(f"📊 Graphique : {extracted_title}")
                
                # 2. On appelle la fonction d'affichage en lui passant le style voulu
                # On utilise 'report_label' pour garantir que les chiffres dépendent du document chargé !
                display_requested_chart("STYLE_BARRES", report_label, chart_key)
                
                chart_rendered = True
            continue  # On ne print pas la ligne contenant la balise brute
            
        # Affichage du texte normal
        else:
            if idx == 0 and "---SECTION_BREAK---" not in lines[0]:
                st.subheader(t["risk_title"])
            st.markdown(line)

    # 3. SÉCURITÉ : Si l'IA a oublié de mettre la balise, on en génère un seul automatiquement
    if not chart_rendered:
        st.markdown("---")
        st.caption("📊 Graphique Complémentaire (Généré automatiquement)")
        display_requested_chart("STYLE_BARRES", report_label, "force_single_chart")
uploaded_file = st.file_uploader(t["choose_pdf"], type="pdf")
st.write(t["example_pdf"])

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
            if st.button(label, use_container_width=True, key=f"btn_ex_{label}"):
                selected_example = path
                selected_example_label = label
                st.session_state["active_label"] = label
        with sub_col2:
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(label="📥", data=f.read(), file_name=os.path.basename(path), mime="application/pdf", key=f"dl_{label}")
            else:
                st.caption("❌")

# --- EXECUTION / AUTO-RELANCE SI LE DOCUMENT EST DÉJÀ INITIALISÉ DANS UNE AUTRE LANGUE ---
if "last_analysis_result" not in st.session_state and "last_analyzed_path" in st.session_state:
    # Déclenchement automatique immédiat lors du changement de langue via l'en-tête
    run_analysis(st.session_state["last_analyzed_path"])

elif selected_example_label is not None and selected_example is not None:
    if not os.path.exists(selected_example):
        if st.session_state["lang"] == "EN":
            st.error(f"File '{selected_example_label}' not found.")
        else:
            st.error(f"Fichier d'exemple introuvable pour '{selected_example_label}'.")
    else:
        run_analysis(selected_example)

elif uploaded_file and st.button(t["btn_analysis"]):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    st.session_state["active_label"] = "Custom Upload"
    run_analysis(tmp_path)
    if os.path.exists(tmp_path): os.unlink(tmp_path)

# Rendu persistant basé sur l'état de session sécurisé
if "last_analysis_result" in st.session_state:
    result = st.session_state["last_analysis_result"]
    active_report = st.session_state.get("active_label", "Analyse")
    st.markdown("---")
    # Appel de la nouvelle fonction pour le graphique unique
    render_dynamic_content_with_single_chart(
        result.get("analysis", ""), 
        result.get("summary", ""), 
        active_report
    ) 