import os
from langchain_groq import ChatGroq

def write_summary(state):
    if isinstance(state, dict):
        analysis = state.get("analysis", "")
    else:
        analysis = state.analysis

    if not isinstance(analysis, str):
        raise ValueError("analysis must be a string")

    prompt = f"""Tu es expert en communication financière.
    Analyse brute des risques :
    {analysis}
    Rédige une synthèse en 3 paragraphes pour un dirigeant non-expert.
    Utilise un langage simple et des exemples concrets."""

    # Remplacement par le modèle actif : llama-3.1-8b-instant
    llm = ChatGroq(
        temperature=0.3,
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )
    
    response = llm.invoke(prompt)
    summary = response.content
    
    return {"summary": summary}