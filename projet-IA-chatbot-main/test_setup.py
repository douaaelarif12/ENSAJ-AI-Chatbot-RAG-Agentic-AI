#!/usr/bin/env python3
"""
Script de test de l'installation du Chatbot ENSAJ
Vérifie que tous les composants sont correctement installés
"""

import sys
import os
from pathlib import Path


def print_header(text):
    """Affiche un en-tête formaté"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def test_python_version():
    """Teste la version de Python"""
    print("🐍 Test de la version Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requis: 3.9+)")
        return False


def test_imports():
    """Teste les imports des packages requis"""
    print("\n📦 Test des packages Python...")
    
    required_packages = [
        ("streamlit", "Streamlit"),
        ("langchain", "LangChain"),
        ("langchain_ollama", "LangChain-Ollama"),
        ("chromadb", "ChromaDB"),
        ("PyPDF2", "PyPDF2"),
        ("dotenv", "python-dotenv"),
        ("ollama", "Ollama Python"),
    ]
    
    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} (manquant)")
            all_ok = False
    
    return all_ok


def test_ollama_connection():
    """Teste la connexion à Ollama"""
    print("\n🔌 Test de connexion Ollama...")
    
    try:
        import ollama
        models = ollama.list()
        print(f"   ✅ Connexion OK")
        
        # Vérifier les modèles requis
        print("\n🤖 Vérification des modèles Ollama...")
        model_names = [m['name'] for m in models.get('models', [])]
        
        required_models = [
            ("gemma2:2b", "Modèle LLM"),
            ("nomic-embed-text:latest", "Modèle Embeddings")
        ]
        
        all_models_ok = True
        for model, desc in required_models:
            if any(model in m for m in model_names):
                print(f"   ✅ {desc}: {model}")
            else:
                print(f"   ❌ {desc}: {model} (manquant)")
                print(f"      → Installer avec: ollama pull {model}")
                all_models_ok = False
        
        return all_models_ok
        
    except Exception as e:
        print(f"   ❌ Connexion échouée: {e}")
        print(f"      → Vérifiez qu'Ollama est lancé: ollama serve")
        return False


def test_project_structure():
    """Vérifie la structure du projet"""
    print("\n📁 Vérification de la structure du projet...")
    
    required_items = [
        ("src/", True, "Dossier source"),
        ("src/__init__.py", False, "Package src"),
        ("src/llm_config.py", False, "Configuration LLM"),
        ("src/vector_store.py", False, "Gestionnaire vector store"),
        ("src/tools.py", False, "Outils de l'agent"),
        ("src/agents.py", False, "Agent IA"),
        ("app.py", False, "Application principale"),
        ("requirements.txt", False, "Dépendances"),
        (".env.example", False, "Configuration exemple"),
        ("data/", True, "Dossier data"),
    ]
    
    all_ok = True
    for item, is_dir, desc in required_items:
        path = Path(item)
        exists = path.is_dir() if is_dir else path.is_file()
        
        if exists:
            print(f"   ✅ {desc}: {item}")
        else:
            print(f"   ❌ {desc}: {item} (manquant)")
            all_ok = False
    
    return all_ok


def test_env_file():
    """Vérifie le fichier .env"""
    print("\n⚙️  Vérification du fichier .env...")
    
    if Path(".env").exists():
        print("   ✅ Fichier .env existe")
        return True
    else:
        print("   ⚠️  Fichier .env manquant")
        print("      → Créer depuis: cp .env.example .env")
        return False


def test_data_folder():
    """Vérifie le dossier data et les PDFs"""
    print("\n📄 Vérification du dossier data...")
    
    data_path = Path("data")
    
    if not data_path.exists():
        print("   ❌ Dossier data manquant")
        return False
    
    pdf_files = list(data_path.glob("*.pdf"))
    
    if pdf_files:
        print(f"   ✅ {len(pdf_files)} fichier(s) PDF trouvé(s):")
        for pdf in pdf_files[:5]:  # Afficher max 5
            print(f"      - {pdf.name}")
        if len(pdf_files) > 5:
            print(f"      ... et {len(pdf_files) - 5} autre(s)")
        return True
    else:
        print("   ⚠️  Aucun fichier PDF trouvé")
        print("      → Ajoutez des PDFs dans le dossier data/")
        return False


def test_vector_store():
    """Teste la création d'un vector store (optionnel)"""
    print("\n🗄️  Test du vector store (optionnel)...")
    
    try:
        from src.vector_store import vector_store_manager
        
        # Juste vérifier que le module se charge
        print("   ✅ Module vector_store OK")
        
        # Si la base existe déjà
        if Path("chroma_db").exists():
            print("   ℹ️  Base vectorielle existante détectée")
        else:
            print("   ℹ️  Aucune base vectorielle (sera créée au premier lancement)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print_header("Test de l'installation - Chatbot ENSAJ")
    
    results = {
        "Python": test_python_version(),
        "Packages": test_imports(),
        "Ollama": test_ollama_connection(),
        "Structure": test_project_structure(),
        "Env": test_env_file(),
        "Data": test_data_folder(),
        "VectorStore": test_vector_store(),
    }
    
    print_header("Résumé des tests")
    
    for name, result in results.items():
        status = "✅ OK" if result else "❌ ERREUR"
        print(f"   {status}  {name}")
    
    print()
    
    all_ok = all(results.values())
    
    if all_ok:
        print("🎉 Tous les tests sont passés!")
        print("\n📝 Prochaines étapes:")
        print("   1. Assurez-vous qu'Ollama est lancé: ollama serve")
        print("   2. Lancez l'application: streamlit run app.py")
        print("   3. Ou utilisez: ./start.sh (Linux/Mac) ou start.bat (Windows)")
        return 0
    else:
        print("⚠️  Certains tests ont échoué.")
        print("\n📝 Actions recommandées:")
        
        if not results["Python"]:
            print("   - Installer Python 3.9+")
        
        if not results["Packages"]:
            print("   - Installer les dépendances: pip install -r requirements.txt")
        
        if not results["Ollama"]:
            print("   - Installer Ollama: https://ollama.ai/download")
            print("   - Télécharger les modèles:")
            print("       ollama pull gemma2:2b")
            print("       ollama pull nomic-embed-text:latest")
        
        if not results["Env"]:
            print("   - Créer le fichier .env: cp .env.example .env")
        
        if not results["Data"]:
            print("   - Ajouter des fichiers PDF dans le dossier data/")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
