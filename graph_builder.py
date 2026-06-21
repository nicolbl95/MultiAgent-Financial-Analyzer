import os
import sys

# Injection de sécurité pour s'assurer que Python trouve le dossier des agents
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Any, TypedDict
from langgraph.graph import StateGraph, END

# Import des agents
from agents.extractor import extract_and_store
from agents.analyzer import analyze_risks
from agents.writer import write_summary

# 1. Définition de la structure de l'état partagé (State)
class AgentState(TypedDict, total=False):
    pdf_path: str
    raw_text: str
    analysis: str
    summary: str
    language: str
    target_language: str
    current_language: str
    system_instruction: str
    instructions: str

# 2. Fonction maîtresse qui construit et compile le graphe d'agents
def build_graph():
    workflow = StateGraph(AgentState)

    # Déclaration des nœuds du graphe
    workflow.add_node("extractor", extract_and_store)
    workflow.add_node("analyzer", analyze_risks)
    workflow.add_node("writer", write_summary)

    # Définition des connexions séquentielles (Edges)
    workflow.set_entry_point("extractor")
    workflow.add_edge("extractor", "analyzer")
    workflow.add_edge("analyzer", "writer")
    workflow.add_edge("writer", END)

    # Compilation du graphe
    return workflow.compile()