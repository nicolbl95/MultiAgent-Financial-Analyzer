import importlib
import os
import shutil
from dotenv import load_dotenv

load_dotenv()


def import_chatgroq():
    try:
        module = importlib.import_module("langchain_groq")
        return getattr(module, "ChatGroq", None)
    except ImportError:
        return None


def import_ollama_llm():
    try:
        module = importlib.import_module("langchain_ollama")
        return getattr(module, "OllamaLLM", None)
    except ImportError:
        return None


def get_writer_llm():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    ChatGroq = import_chatgroq()
    OllamaLLM = import_ollama_llm()

    if ChatGroq is not None and groq_api_key:
        return ChatGroq(
            temperature=0.95,
            model_name="llama-3.1-8b-instant",
            groq_api_key=groq_api_key,
        )

    if OllamaLLM is not None and shutil.which("ollama"):
        return OllamaLLM(model="llama3")

    return None


def write_summary(state):
    # 1. Récupération sécurisée du texte de l'analyse et de la langue d'état (FR par défaut)
    if isinstance(state, dict):
        analysis = state.get("analysis", "")
        lang = state.get("language", "FR")
    else:
        analysis = state.analysis
        lang = getattr(state, "language", "FR")

    # 2. Cartographie de la langue cible pour donner une instruction explicite au LLM
    lang_mapping = {
        "FR": "français (French)",
        "EN": "anglais (English)",
        "ES": "espagnol (Spanish)"
    }
    target_language_name = lang_mapping.get(lang, "français (French)")

    # 3. PROMPT MODIFIÉ : Instruction impérative sur la langue dès le début
    prompt = f"""You are a world-class financial communication expert.
CRITICAL LANGUAGE DIRECTIVE: You must write the entire output, response, headers, and executive summary exclusively in {target_language_name}. Do NOT use any other language.

À partir de l'analyse détaillée des risques ci-dessous, rédige une synthèse exécutive (Summary) claire, concise et percutante.
Structure ta réponse sous forme de paragraphes fluides (pas de style haché ligne par ligne).

CRITIQUE : Tu DOIS enrichir visuellement cette synthèse pour le comité en y insérant de manière pertinente 1 balise graphique (qui n'a pas encore été exploitée dans l'analyse brute ou qui vient appuyer ta conclusion majeure) sur sa propre ligne :
- [GRAPH_EVOLUTION] (Trajectoire et croissance)
- [GRAPH_REPARTITION] (Structure financière et répartition)
- [GRAPH_PERFORMANCE] (Indicateurs clés et rentabilité)

Analyse détaillée :
{analysis}"""

    summary_genere = None
    llm = get_writer_llm()

    if llm is not None:
        try:
            response = llm.invoke(prompt)
            summary_genere = response if isinstance(response, str) else getattr(response, "content", str(response))
        except Exception:
            summary_genere = None

    # 4. Message de secours traduit dynamiquement selon la langue de l'utilisateur
    if not summary_genere:
        if lang == "EN":
            summary_genere = "### Executive Summary Backup\n\nThe analysis highlights key points extracted from the risk assessment report."
        elif lang == "ES":
            summary_genere = "### Resumen Ejecutivo de Reserva\n\nEl análisis destaca los puntos clave extraídos en el informe de análisis de riesgos."
        else:
            summary_genere = "### Synthèse Exécutive de Secours\n\nL'analyse met en évidence les points clés extraits dans le rapport d'analyse des risques."

    return {"summary": summary_genere}