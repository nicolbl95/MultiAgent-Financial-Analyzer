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
    # 1. Récupération sécurisée du texte de l'analyse, du texte brut et de la langue (FR par défaut)
    if isinstance(state, dict):
        analysis = state.get("analysis", "")
        raw_text = state.get("raw_text", "")
        lang = state.get("language", "FR")
    else:
        analysis = state.analysis
        raw_text = getattr(state, "raw_text", "")
        lang = getattr(state, "language", "FR")

    # --- SÉCURITÉ ANTI-PERTE D'ÉTAT ---
    # Si l'état 'language' a été vidé par un agent précédent, on vérifie la consigne système dans le texte
    if "TARGET_LANGUAGE=English" in raw_text or lang == "EN":
        lang = "EN"
    else:
        lang = "FR"
    # ----------------------------------

    # 2. Cartographie de la langue cible pour donner une instruction explicite au LLM
    lang_mapping = {
        "FR": "français (French)",
        "EN": "anglais (English)"
    }
    target_language_name = lang_mapping.get(lang, "français (French)")

    # 3. PROMPT MODIFIÉ : Instruction impérative sur la langue et le graphique unique
    prompt = f"""You are a world-class financial communication expert.
CRITICAL LANGUAGE DIRECTIVE: You must write the entire output, response, headers, and executive summary exclusively in {target_language_name}. Do NOT use any other language.

À partir de l'analyse détaillée des risques ci-dessous, rédige une synthèse exécutive (Summary) claire, concise et percutante.
Structure ta réponse sous forme de paragraphes fluides (pas de style haché ligne par ligne).

CRITIQUE : Tu DOIS enrichir visuellement cette synthèse en y insérant EXACTEMENT 1 seule balise graphique personnalisée sur sa propre ligne. 
Cette balise doit être unique et liée aux chiffres réels du texte. Génère-la sous ce format exact :
[DYNAMIC_GRAPH:Type_De_Donnée_Clé_Ici] (Exemple : [DYNAMIC_GRAPH:Evolution_CA_2025_2026] ou [DYNAMIC_GRAPH:Repartition_Dette])

Ne propose AUCUN autre graphique générique. 1 seul graphique sur mesure est toléré.

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
        else:
            summary_genere = "### Synthèse Exécutive de Secours\n\nL'analyse met en évidence les points clés extraits dans le rapport d'analyse des risques."

    return {"summary": summary_genere} 