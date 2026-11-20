#!/bin/bash

# Script de démarrage rapide pour le Chatbot ENSAJ
# Usage: ./start.sh

echo "🎓 Démarrage du Chatbot ENSAJ..."
echo ""

# Vérifier si Ollama est installé
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama n'est pas installé."
    echo "📥 Veuillez installer Ollama depuis: https://ollama.ai/download"
    exit 1
fi

echo "✅ Ollama est installé"

# Vérifier si les modèles sont disponibles
echo "🔍 Vérification des modèles Ollama..."

if ! ollama list | grep -q "gemma2:2b"; then
    echo "⚠️  Le modèle gemma2:2b n'est pas installé"
    echo "📥 Téléchargement en cours... (1.6 GB)"
    ollama pull gemma2:2b
fi

if ! ollama list | grep -q "nomic-embed-text"; then
    echo "⚠️  Le modèle nomic-embed-text n'est pas installé"
    echo "📥 Téléchargement en cours... (274 MB)"
    ollama pull nomic-embed-text:latest
fi

echo "✅ Tous les modèles sont disponibles"
echo ""

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer/mettre à jour les dépendances
echo "📚 Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier le fichier .env
if [ ! -f ".env" ]; then
    echo "⚙️  Création du fichier .env..."
    cp .env.example .env
fi

# Vérifier le dossier data
if [ ! -d "data" ]; then
    echo "📁 Création du dossier data..."
    mkdir data
fi

# Compter les PDFs
pdf_count=$(find data -name "*.pdf" 2>/dev/null | wc -l)
echo "📄 $pdf_count fichier(s) PDF trouvé(s) dans data/"

if [ $pdf_count -eq 0 ]; then
    echo "⚠️  Aucun PDF trouvé. Veuillez ajouter des PDFs dans le dossier data/"
fi

echo ""
echo "🚀 Lancement de l'application Streamlit..."
echo "📍 L'application s'ouvrira dans votre navigateur à: http://localhost:8501"
echo ""
echo "Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""

# Lancer Streamlit
streamlit run app.py
