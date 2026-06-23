# 📊 Assistant IA Multi-Agents — Analyse Financière

![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-7B3FE4?style=for-the-badge&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-121212?style=for-the-badge&logo=langchain&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C1E26?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0073EC?style=for-the-badge&logo=databricks&logoColor=white)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-7B3FE4?style=for-the-badge&logoColor=white)
![PyPDF](https://img.shields.io/badge/PyPDF-FF6B6B?style=for-the-badge&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Groq API](https://img.shields.io/badge/Groq_API-00D4AA?style=for-the-badge&logo=groq&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Description
Application web **conteneurisée avec Docker** qui analyse automatiquement des rapports financiers PDF
grâce à une architecture multi-agents (LangGraph + LangChain + RAG + ChromaDB).
L'application permet aux utilisateurs de télécharger des PDF ou de sélectionner des exemples prédéfinis pour une analyse immédiate.

## Technologies utilisées
### **Outils de développement**
- **Python 3.14** : Langage principal.
- **VS Code** : Éditeur de code.

### **Orchestration & IA**
- **LangGraph** : Orchestration des agents IA (workflows multi-agents).
- **LangChain** : Framework pour intégrer les LLM et outils (ex: ChromaDB, PDF Loader).
- **RAG (Retrieval-Augmented Generation)** : Architecture pour enrichir les réponses avec des données externes.

### **Modèles de Langage (LLM)**
- **Ollama (Llama 3)** : LLM local pour l’analyse hors ligne.
- **Groq API** : LLM cloud pour le déploiement (accélération matérielle).

### **Base de données & Traitement**
- **ChromaDB** : Base de données vectorielle pour stocker les *embeddings* des PDF.
- **Sentence Transformers** : Génération d’*embeddings* pour le RAG.
- **PyPDF** : Parsing des fichiers PDF.

### **Interface & Déploiement**
- **Streamlit** : Interface web interactive.
- **Docker** : Conteneurisation pour un déploiement portable.

## 🚀 Comment lancer le projet

### **Prérequis**
- **Python 3.14** installé (vérifiez avec `python --version`).
- **Ollama** installé (pour une utilisation locale) : [Télécharger Ollama](https://ollama.com).
- **Docker** (optionnel, pour une exécution conteneurisée) : [Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop).

---

### **Étapes d'installation et d'exécution**

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/nicolbl95/MultiAgent-Financial-Analyzer

   cd MultiAgent-Financial-Analyzer
