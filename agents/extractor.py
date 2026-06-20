from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

def extract_and_store(state):
    # 1. On extrait proprement le chemin du fichier depuis le dictionnaire d'état de LangGraph
    if isinstance(state, dict):
        pdf_path = state.get("pdf_path")
    else:
        pdf_path = state.pdf_path

    if not isinstance(pdf_path, str) or not pdf_path:
        raise ValueError("pdf_path must be a non-empty string")

    # 2. Chargement et découpage du PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)
    
    # 3. Initialisation de ChromaDB et NETTOYAGE de la mémoire
    client = chromadb.Client()
    
    # SÉCURITÉ ANTI-CHEVAUCHEMENT : Supprime l'ancienne collection si elle existe déjà
    try:
        client.delete_collection("financial_doc")
    except Exception:
        # Si la collection n'existait pas encore (premier lancement), on ignore poliment l'erreur
        pass
    
    # Création d'une collection vierge et propre
    collection = client.create_collection("financial_doc")
    
    # Extraction de l'intégralité du texte pour le transmettre à l'état
    full_text = ""
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk.page_content],
            ids=[f"chunk_{i}"]
        )
        full_text += chunk.page_content + "\n"
        
    # 4. On retourne un dictionnaire contenant le texte extrait pour mettre à jour l'état partagé du graphe
    return {"raw_text": full_text}