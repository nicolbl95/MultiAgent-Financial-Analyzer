import os
import chromadb
from langchain_groq import ChatGroq

def analyze_risks(state):
    # 1. Récupérer l'état
    if isinstance(state, dict):
        raw_text = state.get("raw_text", "")
    else:
        raw_text = state.raw_text

    # 2. Connexion à ChromaDB
    client = chromadb.Client()
    collection = client.get_or_create_collection("financial_doc")

    # 3. Requête RAG
    results = collection.query(
        query_texts=["risques financiers, dépendances, réglementation, change"],
        n_results=5
    )
    
    documents = results.get("documents") or []
    documents_trouves = documents[0] if documents else []
    
    # NETTOYAGE : On fusionne les lignes et on supprime les sauts de ligne anarchiques
    contexte_propre = " ".join([doc.replace("\n", " ").strip() for doc in documents_trouves])

    # 4. On demande à Groq de rédiger une VRAIE analyse propre pour éliminer le style haché
    llm = ChatGroq(
        temperature=0.2,
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )
    
    prompt = f"""Tu es un analyste financier senior. Sur la base uniquement du contexte extrait ci-dessous, 
    rédige un rapport d'analyse structuré listant précisément les risques identifiés. 
    Fais des phrases complètes, fluides et horizontales.

    Contexte extrait :
    {contexte_propre}"""
    
    try:
        response = llm.invoke(prompt)
        analyse_generee = response.content
    except Exception as e:
        # En cas de problème d'API, repli sur un texte nettoyé manuellement
        analyse_generee = f"### Analyse des Risques (Mode brut nettoyé)\n\n{contexte_propre}"

    # 5. Mise à jour de l'état
    return {"analysis": analyse_generee}