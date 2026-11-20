# 🚀 Guide de démarrage rapide - Chatbot ENSAJ

Guide pour démarrer rapidement en 5 minutes !

## ⚡ Installation Express

### 1️⃣ Installer Ollama

**Linux/Mac :**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows :**
Télécharger depuis : https://ollama.ai/download

### 2️⃣ Télécharger les modèles (requis)

```bash
# Modèle LLM (1.6 GB) - OBLIGATOIRE
ollama pull gemma2:2b

# Modèle Embeddings (274 MB) - OBLIGATOIRE
ollama pull nomic-embed-text:latest
```

### 3️⃣ Installer les dépendances Python

```bash
# Créer environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Installer les packages
pip install -r requirements.txt
```

### 4️⃣ Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env

# Pas besoin de modifier .env si vous utilisez les valeurs par défaut
```

### 5️⃣ Ajouter vos PDFs

```bash
# Créer le dossier data (si nécessaire)
mkdir -p data

# Copier vos PDFs
cp /chemin/vers/vos/pdfs/*.pdf data/
```

## 🎯 Lancement

### Méthode 1 : Scripts automatiques (recommandé)

**Linux/Mac :**
```bash
chmod +x start.sh
./start.sh
```

**Windows :**
Double-cliquer sur `start.bat` ou :
```cmd
start.bat
```

### Méthode 2 : Manuel

```bash
# 1. S'assurer qu'Ollama est lancé
ollama serve

# 2. (Dans un autre terminal) Activer l'environnement
source venv/bin/activate  # ou venv\Scripts\activate

# 3. Lancer Streamlit
streamlit run app.py
```

## 📱 Utilisation

1. **Ouvrir le navigateur** : http://localhost:8501

2. **Charger la base** :
   - Cliquer sur "📦 Charger la base" dans la barre latérale
   - Attendre quelques secondes (première fois : quelques minutes)

3. **Poser une question** :
   ```
   Quelles sont les filières disponibles à l'ENSAJ ?
   ```

## ✅ Vérifier l'installation

```bash
# Tester l'installation complète
python test_setup.py
```

Ce script vérifie :
- ✅ Version Python
- ✅ Packages installés
- ✅ Connexion Ollama
- ✅ Modèles disponibles
- ✅ Structure du projet
- ✅ Fichiers de configuration

## 🔧 Dépannage Express

### Problème : "Ollama connection failed"

**Solution :**
```bash
# Vérifier qu'Ollama tourne
ollama list

# Si pas de réponse, lancer Ollama
ollama serve
```

### Problème : "No module named 'streamlit'"

**Solution :**
```bash
# Vérifier que l'environnement virtuel est activé
which python  # Doit pointer vers venv/

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème : "Modèle non trouvé"

**Solution :**
```bash
# Vérifier les modèles installés
ollama list

# Télécharger les modèles manquants
ollama pull gemma2:2b
ollama pull nomic-embed-text:latest
```

### Problème : "Aucun document PDF trouvé"

**Solution :**
```bash
# Vérifier le contenu du dossier data
ls -la data/

# Ajouter des PDFs
cp /chemin/vers/vos/pdfs/*.pdf data/
```

### Problème : Port 8501 déjà utilisé

**Solution :**
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

## 📊 Exemples de questions

```
1. "Quelles sont les filières disponibles à l'ENSAJ ?"

2. "Quelle est la durée du cycle ingénieur ?"

3. "Comment contacter l'administration ?"

4. "Quels sont les prérequis pour la filière ISIC ?"

5. "Calcule 125 * 8 + 45"
```

## 🎨 Configuration rapide

### Changer le mode

Dans la barre latérale :
- **🧠 Agent avec outils** : Plus intelligent, raisonnement avancé
- **⚡ RAG simple** : Plus rapide, recherche directe

### Ajuster la créativité

Slider "Température" dans la barre latérale :
- **0.0** : Très déterministe (recommandé pour questions factuelles)
- **0.3** : Équilibré (par défaut)
- **0.7+** : Plus créatif

### Affichage

Cocher "Montrer les étapes de raisonnement" pour voir :
- Quels outils l'agent utilise
- Comment il raisonne
- Les sources consultées

## 📚 Ressources

- **README complet** : `README.md`
- **Documentation data** : `data/README.md`
- **Test installation** : `python test_setup.py`
- **Ollama docs** : https://ollama.ai/docs
- **LangChain docs** : https://python.langchain.com/docs

## 🆘 Besoin d'aide ?

1. **Consulter le README** : Documentation complète avec troubleshooting
2. **Tester l'installation** : `python test_setup.py`
3. **Vérifier les logs** : Messages dans le terminal
4. **Ollama status** : `ollama list` et `ollama ps`

## 🎓 Prochaines étapes

Une fois que tout fonctionne :

1. **Personnaliser les outils** : Éditer `src/tools.py`
2. **Ajuster le prompt** : Modifier `src/agents.py`
3. **Ajouter plus de PDFs** : Compléter le dossier `data/`
4. **Explorer les options** : Tester les différents modes et paramètres

Bon chatbot ! 🚀
