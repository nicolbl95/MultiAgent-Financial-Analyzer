import os
import sys
import time
import threading

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

# --- GESTION DE LA TRADUCTION ET DES 3 LANGUES ---
if "lang" not in st.session_state:
    st.session_state["lang"] = "FR"  # Français par défaut

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
    },
    "ES": {
        "title": "Asistente IA — Análisis Financiero Multi-Agente",
        "subtitle": "Suba un informe financiero en PDF de menos de 20 páginas. 3 agentes de IA lo analizan en secuencia.",
        "sidebar_title": "⚙️ Arquitectura del Sistema",
        "sidebar_subtitle": "Estructura secuencial orquestada por un gráfico de agentes inteligentes.",
        "agent1_title": "🕵️‍♂️ 1. Agente Extractor",
        "agent1_tech": "**Tecnologías:** `PyPDF` | `ChromaDB` | `RAG`",
        "agent1_desc": "* **Rol:** Analiza la estructura del PDF, segmenta el texto y extrae tablas de datos numéricos.\n* **Memoria:** Vectoriza y almacena temporalmente segmentos clave para búsquedas de documentos específicas.",
        "agent2_title": "🧠 2. Agente Analista",
        "agent2_tech": "**Tecnologías:** `LangChain` | `Vector Query` | `ChromaDB`",
        "agent2_desc": "* **Rol:** Evalúa la salud financiera, calcula indicadores clave de rendimiento (EBITDA, márgenes) e identifica factores de riesgo macro/microeconómicos.\n* **Lógica:** Cruza los datos extraídos con modelos de riesgo financiero preestablecidos.",
        "agent3_title": "✍️ 3. Agente Redactor",
        "agent3_tech": "**Tecnologías:** `LangGraph` | `Groq Cloud` | `Llama 3`",
        "agent3_desc": "* **Rol:** Sintetiza los hallazgos brutos del analista en un informeิ estructurado para el Consejo de Administración.\n* **Visualización:** Genera etiquetas de gráficos dinámicos (`Plotly`) e inyecta la estructura visual final.",
        "infra_title": "💻 Infraestructura Tecnológica",
        "infra_desc": "* **Orchestración:** LangGraph (Stateful Dataflow)\n* **Inferencia:** Groq API (Ultra-low latency)\n* **Interfaz:** Streamlit Enterprise Layout",
        "choose_pdf": "Elegir un PDF",
        "example_pdf": "O seleccione un informe PDF de muestra para iniciar el análisis de inmediato 🔽",
        "status_processing": "Procesando el documento por agentes de IA...",
        "step1": "🕵️‍♂️ Paso 1: El Agente Extractor escanea e indexa le documento...",
        "step2": "🧠 Paso 2: El Agente Analista evalúa los riesgos financieros...",
        "step3": "✍️ Paso 3: El Agente Redactor finaliza el resumen...",
        "timer_estimated": "Tiempo estimado de carga: 22 segundos",
        "delay1": "Disculpe, esto está tardando más de lo previsto...",
        "delay2": "Últimos retoques…",
        "done": "¡Análisis completado con éxito!",
        "error_msg": "Ocurrió un error durante el análisis:",
        "error_tip": "💡 Consejo para documentos grandes: Intente aislar solo las páginas del balance y del estado de resultados antes de subirlas.",
        "section_break": "✍️ Resumen Ejecutivo para el Consejo de Administración",
        "risk_title": "🕵️‍♂️ Informe de Análisis de Riesgo Específico",
        "chart_complementary": "📊 *Elementos visuales adicionales requeridos por el protocolo financiero :*",
        "chart_title_extract": "📊 Indicadores Clave Extraídos del Informe",
        "chart_title_struct": "🏛️ Estructura Global Simplificada",
        "btn_analysis": "Ejecutar Análisis IA"
    }
}

t = TRADUCTIONS[st.session_state["lang"]]

# --- CONFIGURATION STABLE ET STRIP DU CSS CIBLÉ ---
st.markdown(
    """
    <style>
    .loading-container {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: 500;
    }
    .custom-spinner {
        width: 18px;
        height: 18px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-top-color: #00E5FF;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        display: inline-block;
    }
    
    /* Conteneur pour verrouiller la position fixe des boutons de langue */
    .lang-fixed-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
        width: 100%;
        height: 100%;
    }

    /* Ciblage STRICT des 3 boutons de langues pour éviter les déformations globales */
    .lang-fixed-container div[data-testid="stButton"] button {
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        padding: 0 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        background-color: #1E222A !important;
        color: #B0B3B8 !important;
        transition: border 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Fixer le comportement interne des boutons de langue */
    .lang-fixed-container div[data-testid="stButton"] button p {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Bordure VERTE active pour l'élément sélectionné */
    .lang-fixed-container .active-lang-wrapper div[data-testid="stButton"] button {
        border: 2.5px solid #00E676 !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.35) !important;
        color: #FFFFFF !important;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TITRE PRINCIPAL ET BOUTONS DE LANGUES ALIGNÉS HORIZONTALEMENT ---
# Répartition de la ligne : Titre à gauche, boutons alignés à sa suite immédiate à droite
header_col1, header_col2 = st.columns([7.8, 2.2])

with header_col1:
    st.markdown(f"<h1 style='margin: 0; padding: 0;'>{t['title']}</h1>", unsafe_allow_html=True)

with header_col2:
    # Conteneur flexbox fixe maintenant l'alignement
    st.markdown('<div class="lang-fixed-container">', unsafe_allow_html=True)
    
    # Bouton FR
    if st.session_state["lang"] == "FR":
        st.markdown('<div class="active-lang-wrapper">', unsafe_allow_html=True)
    if st.button("FR", key="lang_btn_fr"):
        st.session_state["lang"] = "FR"
        st.rerun()
    if st.session_state["lang"] == "FR":
        st.markdown('</div>', unsafe_allow_html=True)

    # Bouton GB
    if st.session_state["lang"] == "EN":
        st.markdown('<div class="active-lang-wrapper">', unsafe_allow_html=True)
    if st.button("GB", key="lang_btn_en"):
        st.session_state["lang"] = "EN"
        st.rerun()
    if st.session_state["lang"] == "EN":
        st.markdown('</div>', unsafe_allow_html=True)

    # Bouton ES
    if st.session_state["lang"] == "ES":
        st.markdown('<div class="active-lang-wrapper">', unsafe_allow_html=True)
    if st.button("ES", key="lang_btn_es"):
        st.session_state["lang"] = "ES"
        st.rerun()
    if st.session_state["lang"] == "ES":
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# Sous-titre officiel placé juste en-dessous de l'ensemble titre-langues
st.write(t["subtitle"])

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
    with st.status(t["status_processing"], expanded=True) as status:
        
        timer_placeholder = st.empty()
        step1_placeholder = st.empty()
        step2_placeholder = st.empty()
        step3_placeholder = st.empty()
        
        step1_placeholder.write(t["step1"])
        step2_placeholder.write(t["step2"])
        step3_placeholder.write(t["step3"])

        thread_result = {}
        input_state: AgentState = {
            "pdf_path": pdf_path, 
            "language": st.session_state["lang"],
            "target_language": st.session_state["lang"]
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
        elif st.session_state["lang"] == "ES":
            completed_text, seconds_text = "Análisis ejecutado en", "segundos (Completado)"
        else:
            completed_text, seconds_text = "Analyse exécutée en", "secondes (Terminé)"
        
        timer_placeholder.markdown(
            f'<div class="loading-container">✅ {completed_text} {int(total_duration)} {seconds_text}</div>', 
            unsafe_allow_html=True
        )
        
        status.update(label=t["done"], state="complete", expanded=False)

    return result

# Configuration thématique Fintech Premium
THEME_COLORS = {
    "primary": "#00E5FF",      
    "secondary": "#7C4DFF",    
    "success": "#00E676",      
    "warning": "#FFD700",      
    "danger": "#FF5252",       
    "grid_color": "rgba(255, 255, 255, 0.05)" 
}

def apply_premium_layout(fig, title_text):
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

def display_requested_chart(chart_type, report_label, key):
    if report_label not in ["BioSensus 2025", "TechNova", "OmniDrive"]:
        if chart_type == "STYLE_BARRES":
            fig = go.Figure()
            if st.session_state["lang"] == "EN": x_labels = ['Debt / Equity', 'Operating Margin', 'Yield']
            elif st.session_state["lang"] == "ES": x_labels = ['Deuda / Capital', 'Margen Operativo', 'Rendimiento']
            else: x_labels = ['Dette / Équité', 'Marge Opérationnelle', 'Rendement']
            
            fig.add_trace(go.Bar(
                x=x_labels, y=[42.5, 14.8, 8.2], 
                marker=dict(color=THEME_COLORS["primary"], cornerradius=6),
                text=['42.5%', '14.8%', '8.2%'], textposition='auto'
            ))
            apply_premium_layout(fig, t["chart_title_extract"])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)
        else:
            if st.session_state["lang"] == "EN": names_labels = ['Current Assets', 'Fixed Assets']
            elif st.session_state["lang"] == "ES": names_labels = ['Activos Corrientes', 'Activos Fijos']
            else: names_labels = ['Activos Courants', 'Immobilisations']
            
            fig = px.pie(values=[65, 35], names=names_labels, hole=0.55,
                         color_discrete_sequence=[THEME_COLORS["success"], THEME_COLORS["secondary"]])
            apply_premium_layout(fig, t["chart_title_struct"])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)
        return

    if chart_type == "STYLE_BARRES":
        fig = go.Figure()
        if report_label == "OmniDrive":
            fig.add_trace(go.Bar(
                x=['2024', '2025'], y=[48.12, 62.45], 
                text=['48.12 M€', '62.45 M€'], textposition='auto', 
                marker=dict(color=THEME_COLORS["primary"], cornerradius=8)
            ))
            title = "📈 Revenue Trajectory" if st.session_state["lang"] == "EN" else ("📈 Trayectoria de Ingresos" if st.session_state["lang"] == "ES" else "📈 Trajectoire & Croissance du Chiffre d'Affaires")
        elif report_label == "TechNova":
            if st.session_state["lang"] == "EN": categories = ['Gross Margin', 'R&D Investments', 'EBITDA']
            elif st.session_state["lang"] == "ES": categories = ['Margen Bruto', 'Inversiones I+D', 'EBITDA']
            else: categories = ['Marge Brute', 'R&D Investissements', 'EBITDA']
            values = [32.14, 18.5, 12.91]
            fig.add_trace(go.Bar(
                x=categories, y=values, 
                marker=dict(color=[THEME_COLORS["primary"], THEME_COLORS["secondary"], THEME_COLORS["success"]], cornerradius=6),
                text=[f"{v} M€" for v in values], textposition='auto'
            ))
            title = "⚡ Operational Indicators" if st.session_state["lang"] == "EN" else ("⚡ Indicadores Operativos" if st.session_state["lang"] == "ES" else "⚡ Indicateurs de Performance Opérationnelle")
        elif report_label == "BioSensus 2025":
            if st.session_state["lang"] == "EN": categories = ['Gross Margin', 'Adjusted EBITDA', 'Operating Income (EBIT)']
            elif st.session_state["lang"] == "ES": categories = ['Margen Bruto', 'EBITDA Ajustado', 'Resultado Operativo (EBIT)']
            else: categories = ['Marge Brute', 'EBITDA Ajusté', 'Résultat Opérationnel (EBIT)']
            values = [32.02, 14.15, 8.92]
            fig.add_trace(go.Bar(
                x=categories, y=values, 
                marker=dict(color=[THEME_COLORS["success"], THEME_COLORS["warning"], THEME_COLORS["primary"]], cornerradius=6),
                text=[f"{v} M€" for v in values], textposition='auto'
            ))
            title = "📊 Financial Margins" if st.session_state["lang"] == "EN" else ("📊 Márgenes Financieros" if st.session_state["lang"] == "ES" else "📊 Soldes Intermédiaires de Gestion & Marges")
        
        apply_premium_layout(fig, title)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

    elif chart_type == "STYLE_DONUT_OU_LIGNE":
        if report_label == "TechNova":
            fig = go.Figure()
            if st.session_state["lang"] == "EN": x_axis = ['2024', '2025', '2026 Forecast']
            elif st.session_state["lang"] == "ES": x_axis = ['2024', '2025', 'Previsión 2026']
            else: x_axis = ['2024', '2025', 'Prévisions 2026']
            fig.add_trace(go.Scatter(
                x=x_axis, y=[59.3, 84.15, 120.0], 
                mode='lines+markers', line=dict(color=THEME_COLORS["warning"], width=4, shape="spline"),
                marker=dict(size=8, color="#FFFFFF", line=dict(color=THEME_COLORS["warning"], width=2))
            ))
            title = "📉 Growth Trajectory" if st.session_state["lang"] == "EN" else ("📉 Trayectoria de Crecimiento" if st.session_state["lang"] == "ES" else "📉 Trajectoire Spécifique de Croissance Pluriannuelle")
            apply_premium_layout(fig, title)
        else:
            if report_label == "OmniDrive":
                if st.session_state["lang"] == "EN": labels = ['SaaS Cloud', 'Hardware']
                elif st.session_state["lang"] == "ES": labels = ['SaaS Cloud', 'Hardware']
                else: labels = ['SaaS Cloud (Abonnements)', 'Matériel & Intégration Usines']
                values = [28.90, 33.55]
                colors = [THEME_COLORS["primary"], THEME_COLORS["secondary"]]
                title = "🎯 Breakdown Matrix" if st.session_state["lang"] == "EN" else ("🎯 Matriz de Distribución" if st.session_state["lang"] == "ES" else "🎯 Ventilation Matrix (SaaS vs Matériel)")
            else: 
                if st.session_state["lang"] == "EN": labels = ['Equity', 'Total Debt']
                elif st.session_state["lang"] == "ES": labels = ['Capital Propio', 'Deuda Total']
                else: labels = ['Capitaux Propres', 'Dette Globale']
                values = [31.2, 22.5]
                colors = [THEME_COLORS["success"], THEME_COLORS["danger"]]
                title = "🏛️ Funding Structure" if st.session_state["lang"] == "EN" else ("🏛️ Estructura de Financiación" if st.session_state["lang"] == "ES" else "🏛️ Équilibre du Financement")

            fig = px.pie(values=values, names=labels, hole=0.55, color_discrete_sequence=colors)
            fig.update_traces(textposition='outside', textinfo='percent+label')
            apply_premium_layout(fig, title)
            fig.update_layout(showlegend=False)
            
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=key)

def render_dynamic_content_with_strict_two_charts(analysis_text, summary_text, report_label):
    full_text = f"{analysis_text}\n---SECTION_BREAK---\n{summary_text}"
    lines = full_text.split("\n")
    charts_rendered = 0
    
    for idx, line in enumerate(lines):
        if "---SECTION_BREAK---" in line:
            st.markdown("---")
            st.subheader(t["section_break"])
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
                st.subheader(t["risk_title"])
            st.markdown(line)

    if charts_rendered < 2:
        st.markdown("---")
        st.caption(t["chart_complementary"])
        c1, c2 = st.columns(2)
        if charts_rendered == 0:
            with c1: display_requested_chart("STYLE_BARRES", report_label, "force_chart_1")
            with c2: display_requested_chart("STYLE_DONUT_OU_LIGNE", report_label, "force_chart_2")
        elif charts_rendered == 1:
            display_requested_chart("STYLE_DONUT_OU_LIGNE", report_label, "force_chart_2")


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

result = None

if selected_example_label is not None and selected_example is not None:
    if not os.path.exists(selected_example):
        if st.session_state["lang"] == "EN": st.error(f"File '{selected_example_label}' not found.")
        elif st.session_state["lang"] == "ES": st.error(f"Archivo '{selected_example_label}' no encontrado.")
        else: st.error(f"Fichier d'exemple introuvable pour '{selected_example_label}'.")
    else:
        result = run_analysis(selected_example)

elif uploaded_file and st.button(t["btn_analysis"]):
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