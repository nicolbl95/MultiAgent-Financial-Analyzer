import os
import shutil
import chromadb
from dotenv import load_dotenv
from pydantic import SecretStr

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
            temperature=0.95,
            model="llama-3.1-8b-instant",
            api_key=SecretStr(groq_api_key),
        )

    if OllamaLLM is not None and shutil.which("ollama"):
        return OllamaLLM(model="llama3")

    return None


def analyze_risks(state):
    # 1. Récupération sécurisée du texte brut et de la langue (avec vérification des clés alternatives)
    if isinstance(state, dict):
        raw_text = state.get("raw_text", "")
        lang = state.get("language", "FR")
        if state.get("lang") == "EN" or state.get("target_language") == "EN":
            lang = "EN"
    else:
        raw_text = state.raw_text
        lang = getattr(state, "language", "FR")
        if getattr(state, "lang", "FR") == "EN" or getattr(state, "target_language", "FR") == "EN":
            lang = "EN"

    # 2. Cartographie stricte de la langue cible
    if lang == "EN":
        target_language_name = "English"
        instruction_text = (
            "Based on the extracted data from the document, write a detailed financial and strategic risk analysis of the company.\n"
            "Structure your response with fluent, fully drafted, and professional paragraphs."
        )
    elif lang == "ES":
        target_language_name = "Spanish"
        instruction_text = (
            "A partir de los datos extraídos del documento, redacte un análisis detallado de los riesgos financieros de la empresa.\n"
            "Estructure su respuesta en párrafos fluidos, redactados y profesionales."
        )
    else:
        target_language_name = "French"
        instruction_text = (
            "À partir des données extraites du document, rédige une analyse détaillée des risques financiers de l'entreprise.\n"
            "Structure ta réponse avec des paragraphes fluides, rédigés et professionnels."
        )

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
        # 3. PROMPT CORRIGÉ : Instructions 100% harmonisées dans la langue cible
        # Suppression des anciennes consignes de balises parasites [GRAPH_EVOLUTION]
        prompt = f"""You are a senior financial analyst and risk management expert.
CRITICAL LANGUAGE DIRECTIVE: You MUST write the entire output, response, headers, titles, and professional analysis exclusively in {target_language_name}. Do NOT use any other language than {target_language_name}.

{instruction_text}

Document Data:
{raw_text}"""
        try:
            response = llm.invoke(prompt)
            analyse_generee = response if isinstance(response, str) else getattr(response, "content", str(response))
        except Exception:
            analyse_generee = None

    # 4. Traduction dynamique du mode de secours selon le choix de l'utilisateur
    if not analyse_generee:
        if lang == "EN":
            analyse_generee = (
                "### Risk Analysis (Notice)\n\n"
                "⚠️ *The automated financial analysis for this sample document is currently unavailable in English. "
                "Please read the English Executive Summary generated right below.*"
            )
        elif lang == "ES":
            analyse_generee = (
                "### Análisis de Riesgos (Aviso)\n\n"
                "⚠️ *El análisis financiero automatizado para este documento no está disponible en este momento. "
                "Consulte el Resumen Ejecutivo en la sección siguiente.*"
            )
        else:
            analyse_generee = (
                "### Analyse des Risques (Mode de secours)\n\n"
                "Aucun backend IA disponible ou erreur de génération. Voici le contexte extrait :\n\n"
                f"{contexte_propre}"
            )

    return {"analysis": analyse_generee}