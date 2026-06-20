import os
import shutil
import chromadb
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_ollama import OllamaLLM
except ImportError:
    OllamaLLM = None


def get_analyzer_llm():
    groq_api_key = os.environ.get("GROQ_API_KEY")

    if ChatGroq is not None and groq_api_key:
        return ChatGroq(
            temperature=0.8,
            model_name="llama-3.1-8b-instant",
            groq_api_key=groq_api_key,
        )

    if OllamaLLM is not None and shutil.which("ollama"):
        return OllamaLLM(model="llama3")

    return None


def analyze_risks(state):
    if isinstance(state, dict):
        raw_text = state.get("raw_text", "")
    else:
        raw_text = state.raw_text

    client = chromadb.Client()
    collection = client.get_or_create_collection("financial_doc")

    results = collection.query(
        query_texts=["risques financiers, dépendances, réglementation, change"],
        n_results=5,
    )

    documents = results.get("documents") or []
    documents_trouves = documents[0] if documents else []
    contexte_propre = " ".join([doc.replace("\n", " ").strip() for doc in documents_trouves])

    llm = get_analyzer_llm()
    analyse_generee = None

    if llm is not None:
        prompt = f"""Tu es un analyste financier senior. Sur la base uniquement du contexte extrait ci-dessous,
rédige un rapport d'analyse structuré listant précisément les risques identifiés.
Fais des phrases complètes, fluides et horizontales.

Contexte extrait :
{contexte_propre}"""
        try:
            response = llm.invoke(prompt)
            analyse_generee = response if isinstance(response, str) else getattr(response, "content", str(response))
        except Exception:
            analyse_generee = None

    if not analyse_generee:
        analyse_generee = (
            "### Analyse des Risques (Mode de secours)\n\n"
            "Aucun backend IA disponible ou erreur de génération. Voici le contexte extrait :\n\n"
            f"{contexte_propre}"
        )

    return {"analysis": analyse_generee}