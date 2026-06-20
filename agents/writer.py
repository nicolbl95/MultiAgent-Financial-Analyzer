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
            temperature=0.3,
            model_name="llama-3.1-8b-instant",
            groq_api_key=groq_api_key,
        )

    if OllamaLLM is not None and shutil.which("ollama"):
        return OllamaLLM(model="llama3")

    return None


def write_summary(state):
    if isinstance(state, dict):
        analysis = state.get("analysis", "")
    else:
        analysis = state.analysis

    prompt = f"""Tu es un expert en communication financière auprès de comités de direction.
À partir de l'analyse détaillée des risques ci-dessous, rédige une synthèse exécutive (Summary) claire, concise et percutante.
Structure ta réponse sous forme de paragraphes fluides (pas de style haché ligne par ligne).

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

    if not summary_genere:
        summary_genere = (
            "### Synthèse Exécutive de Secours\n\n"
            "L'analyse met en évidence les points clés extraits dans le rapport d'analyse des risques."
        )

    return {"summary": summary_genere}