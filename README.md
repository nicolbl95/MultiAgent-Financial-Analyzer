# 📊 Assistant IA Multi-Agents — Analyse Financière

![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-7B3FE4?style=for-the-badge&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-121212?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0073EC?style=for-the-badge&logo=databricks&logoColor=white)
![Ollama Llama3](https://img.shields.io/badge/Ollama-Llama_3-black?style=for-the-badge&logo=ollama&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-00D4AA?style=for-the-badge&logo=groq&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)


## Description
Application web qui analyse automatiquement des rapports financiers PDF
grâce à une architecture multi-agents (LangGraph + RAG + ChromaDB).

## Technologies utilisées
- Python 3.14
- RAG (Retrieval-Augmented Generation)
- LangGraph (orchestration d'agents IA)
- ChromaDB (base de données vectorielle / RAG)
- Groq (accélération LLM)
- Ollama — Llama 3 (LLM local)
- Streamlit (interface web)

## Comment lancer le projet
1. Cloner le dépôt : `git clone https://github.com/nicolbl95/First-Project`
2. Créer l'environnement virtuel : `python -m venv venv` puis l'activer
3. Installer les dépendances : `pip install -r requirements.txt`
4. Installer Ollama et télécharger Llama 3 : `ollama pull llama3`
5. Lancer : `streamlit run app.py`

## Démo en ligne
[Lien Streamlit Community Cloud — à ajouter à l'étape 5.3]