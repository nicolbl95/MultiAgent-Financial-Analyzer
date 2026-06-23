# 📊 Assistant IA Multi-Agents — Analyse Financière

![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-121212?style=for-the-badge&logo=langchain&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-7B3FE4?style=for-the-badge&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0073EC?style=for-the-badge&logo=databricks&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Groq API](https://img.shields.io/badge/Groq_API-00D4AA?style=for-the-badge&logo=groq&logoColor=white)
[![🚀 Démo Live](https://img.shields.io/badge/%F0%9F%9A%80_D%C3%A9mo_Live-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://multiagent-financial-analyzer.streamlit.app/)

## Description
Application web **conteneurisée avec Docker** qui analyse automatiquement des rapports financiers PDF grâce à une architecture multi-agents (LangGraph + LangChain + RAG + ChromaDB). L'application permet aux utilisateurs de télécharger des PDF ou de sélectionner des exemples prédéfinis pour une analyse immédiate.

ℹ️ **Démo en ligne :** Vous pouvez tester directement l'application sans aucune installation en vous rendant sur [multiagent-financial-analyzer.streamlit.app](https://multiagent-financial-analyzer.streamlit.app/).

## 📸 Aperçu de l'interface

![Interface de l'application](assets/1dashboard.png)
*Légende : Interface utilisateur Streamlit avec sélection de langue et compteur de temps réel.*

## ✨ Fonctionnalités clés

* 🤖 **Architecture Multi-Agents** : Découpage des tâches et de la logique métier entre un agent extracteur (RAG), un analyste de risques et un rédacteur de synthèses via LangGraph.
* 📊 **Rapports pré-chargés** : Intégration de 3 exemples de rapports réels (*BioSensus, TechNova, OmniDrive*) pour tester l'application instantanément sans téléversement obligatoire.
* 🌍 **Interface Multilingue** : Support natif et complet de l'interface en Français et en Anglais commutable en un clic.
* ⏱️ **Compteur de Temps Réel** : Intégration d'un indicateur de temps estimé pendant l'exécution séquentielle des agents pour optimiser l'expérience utilisateur.

---

## 📂 Structure du projet

L'architecture du code est découpée de manière modulaire afin de respecter les bonnes pratiques d'ingénierie logicielle :

```text
├── .vscode/               # Configuration locale de l'éditeur VS Code
├── agents/                # Agents IA spécialisés autonomes
│   ├── __init__.py
│   ├── analyzer.py        # Agent d'analyse des risques (Ollama/Groq)
│   ├── extractor.py       # Agent d'extraction et chunking PDF (ChromaDB)
│   └── writer.py          # Agent de rédaction de la synthèse managériale
├── assets/                # Images et ressources visuelles du projet
│   └── 1dashboard.png     # Capture d'écran de l'interface applicative
├── sample_reports/        # Les 3 rapports PDF financiers d'exemples
│   ├── Rapport_Financier_Avance_OmniDrive.pdf
│   ├── Rapport_Financier_TechNova.pdf
│   └── Rapport_Performance_BioSensus_2025.pdf
├── utils/                 # Fonctions utilitaires partagées
├── venv/                  # Environnement virtuel local Python
├── .env                   # Variables d'environnement privées (Clés API - Masquées)
├── .gitignore             # Fichiers exclus du suivi de version Git
├── app.py                 # Interface utilisateur et frontend Streamlit
├── graph_builder.py       # Coeur du système : Construction et compilation du graphe LangGraph
├── README.md              # Documentation principale du projet
└── requirements.txt       # Liste complète des dépendances Python requises

🛠️ Technologies utilisées
Outils de développement
Python 3.14 : Langage et runtime de programmation principal.

VS Code : Environnement de développement (IDE).

Orchestration & IA
LangGraph : Modélisation des flux et orchestration cyclique/séquentielle des agents IA.

LangChain : Intégration des connecteurs LLM, chargement de documents et de prompts complexes.

RAG (Retrieval-Augmented Generation) : Indexation sémantique pour nourrir les agents avec les sections du PDF les plus pertinentes.

Modèles de Langage (LLM)
Ollama (Llama 3) : Exécution de LLM en local pour préserver la confidentialité des données financières.

Groq API : Accès Cloud ultra-rapide aux modèles open-source pour les environnements distants et serveurs de démo.

Base de données & Traitement
ChromaDB : Base de données vectorielle permettant de stocker et requêter efficacement les morceaux (chunks) de documents.

Sentence Transformers : Génération locale d'embeddings vectoriels de haute qualité.

PyPDF : Extraction brute et parsing du contenu textuel des rapports financiers.

Interface & Déploiement
Streamlit : Framework de création d'applications web d'IA interactives.

Docker : Conteneurisation de l'application pour garantir un comportement identique d'une machine à une autre.

🚀 Comment lancer le projet
Prérequis
Python 3.14.x (Vérifiez votre installation locale via python --version).

Ollama installé sur votre machine : Télécharger Ollama.

Docker (Optionnel, utile pour lancer l'environnement isolé) : Télécharger Docker Desktop.

Étapes d'installation et d'exécution
Cloner le dépôt :

Bash
git clone [https://github.com/nicolbl95/MultiAgent-Financial-Analyzer](https://github.com/nicolbl95/MultiAgent-Financial-Analyzer)
cd MultiAgent-Financial-Analyzer
Créer et activer l'environnement virtuel :

Bash
python -m venv venv
# Sur Windows (Git Bash / Command Prompt) :
source venv/Scripts/activate
Installer les dépendances :

Bash
pip install -r requirements.txt
Configurer l'environnement local :

Pour Ollama (Local) : Récupérez le modèle Llama 3 en arrière-plan :

Bash
ollama pull llama3
Pour Groq API (Cloud / Optionnel) : Créez un fichier .env à la racine et collez-y votre clé d'accès :

Extrait de code
GROQ_API_KEY=votre_cle_groq_ici
Lancer l'interface Streamlit :

Bash
streamlit run app.py
Exécution via Docker 🐳
Si vous préférez exécuter l'application au sein d'un conteneur Docker léger :

Bash
# Construire l'image Docker
docker build -t financial-analyzer .

# Lancer le conteneur sur le port 8501
docker run -p 8501:8501 financial-analyzer
Rendez-vous ensuite sur http://localhost:8501 depuis votre navigateur internet.