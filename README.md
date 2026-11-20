# 🎓 Chatbot ENSAJ - RAG avec Agentic AI

Chatbot intelligent pour l'École Nationale des Sciences Appliquées d'El Jadida (ENSAJ) utilisant RAG (Retrieval-Augmented Generation) et Agentic AI avec des modèles locaux Ollama.
Réalisé par : Douaa El Arif
## ✨ Caractéristiques

- **Agentic AI** : Agent intelligent avec raisonnement ReAct et utilisation d'outils
-  **RAG (Retrieval-Augmented Generation)** : Réponses basées uniquement sur vos documents
-  **ChromaDB** : Base vectorielle persistante pour recherche sémantique rapide
-  **LLM Local** : Utilise Ollama avec `gemma2:2b` (pas besoin d'API externe)
-  **Embeddings locaux** : `nomic-embed-text:latest` pour vectorisation
-  **Interface Streamlit** : UI moderne et interactive
-  **Outils multiples** : Recherche documentaire, calculs, informations ENSAJ
-  **Persistence** : Base vectorielle sauvegardée automatiquement
-  **Deux modes** : Agent complet ou RAG simple (plus rapide)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Interface Streamlit                      │
│                         (app.py)                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐       ┌───────▼────────┐
        │  Agentic AI    │       │   Simple RAG   │
        │  (avec outils) │       │   (plus rapide)│
        └───────┬────────┘       └───────┬────────┘
                │                        │
                └───────────┬────────────┘
                            │
              ┌─────────────▼─────────────┐
              │    LangChain Framework    │
              └─────────────┬─────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
   │  Ollama  │      │  ChromaDB  │     │   Tools    │
   │  (LLM +  │      │  (Vector   │     │ (Recherche,│
   │ Embeddings)│     │   Store)   │     │  Calcul)   │
   └──────────┘      └────────────┘     └────────────┘
        │                   │
        │              ┌────▼─────┐
        │              │   PDFs   │
        │              │ (/data/) │
        └──────────────┴──────────┘
```

## 🔧 Prérequis

### Logiciels requis

1. **Python 3.10+**
  

2. **Ollama** (pour les modèles locaux)
   - Installation : https://ollama.ai/download
  
### Modèles Ollama requis

Télécharger les modèles nécessaires :

```bash
# Modèle LLM (1.6 GB)
ollama pull gemma2:2b

# Modèle d'embeddings (274 MB)
ollama pull nomic-embed-text:latest
```

Vérifier que les modèles sont installés :

## 📥 Installation

### 1. Cloner ou télécharger le projet

```bash
cd chatbot_ensaj
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur Linux/Mac :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer le fichier .env

```bash
cp .env.example .env
```


### 5. Ajouter vos documents PDF

Placer vos fichiers PDF dans le dossier `data/` :


## 🚀 Utilisation

### Démarrage rapide

1. **S'assurer qu'Ollama est lancé** :
   ```bash
   # Vérifier le service
   ollama list
   
   # Si Ollama n'est pas lancé, le démarrer
   ollama serve
   ```

2. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

3. **Ouvrir dans le navigateur** :
   L'application s'ouvre automatiquement à : http://localhost:8501

### Première utilisation

1. **Charger la base vectorielle** :
   - Cliquer sur "📦 Charger la base" dans la barre latérale
   - Ou cliquer sur "Charger automatiquement la base" dans l'interface principale
   - La première fois, cela peut prendre quelques minutes (création de la base)
   - Les fois suivantes, le chargement sera instantané (base persistée)

2. **Choisir le mode** :
   - **🧠 Agent avec outils** (recommandé) : Raisonnement avancé avec plusieurs outils
   - **⚡ RAG simple** : Recherche directe, plus rapide

3. **Commencer à poser des questions** !

### Exemples de questions

```
- Quelles sont les filières disponibles à l'ENSAJ ?
- Quelle est la durée du cycle ingénieur ?
- Comment contacter l'ENSAJ ?
- Calcule 25 * 48 + 120
- Quelles sont les conditions d'admission ?
```

## 📁 Structure du projet

```
chatbot_ensaj/
│
├── data/                          # 📄 Dossier pour vos PDFs
│   └── *.pdf                      # Vos documents ENSAJ
│
├── chroma_db/                     # 🗄️ Base vectorielle (créée automatiquement)
│   └── ...                        # Données ChromaDB
│
├── src/                           # 📦 Code source modulaire
│   ├── __init__.py               # Package Python
│   ├── llm_config.py             # 🤖 Configuration Ollama
│   ├── vector_store.py           # 🗄️ Gestion ChromaDB
│   ├── tools.py                  # 🛠️ Outils pour l'agent
│   └── agents.py                 # 🧠 Agent IA et RAG
│
├── app.py                         # 🎨 Application Streamlit principale
├── requirements.txt               # 📋 Dépendances Python
├── .env.example                   # ⚙️ Configuration exemple
├── .env                          # ⚙️ Configuration (à créer)
└── README.md                      # 📖 Documentation (ce fichier)
```

