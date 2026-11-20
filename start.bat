@echo off
REM Script de démarrage rapide pour le Chatbot ENSAJ (Windows)
REM Usage: double-cliquer sur start.bat

echo.
echo ==============================================
echo    Chatbot ENSAJ - Demarrage
echo ==============================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python 3.9+ depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python est installe
echo.

REM Vérifier si Ollama est installé
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Ollama n'est pas installe
    echo Veuillez installer Ollama depuis: https://ollama.ai/download
    pause
    exit /b 1
)

echo [OK] Ollama est installe
echo.

REM Vérifier les modèles
echo Verification des modeles Ollama...
echo.

ollama list | findstr "gemma2:2b" >nul
if errorlevel 1 (
    echo [INFO] Telechargement du modele gemma2:2b (1.6 GB)...
    ollama pull gemma2:2b
)

ollama list | findstr "nomic-embed-text" >nul
if errorlevel 1 (
    echo [INFO] Telechargement du modele nomic-embed-text (274 MB)...
    ollama pull nomic-embed-text:latest
)

echo [OK] Tous les modeles sont disponibles
echo.

REM Vérifier/créer l'environnement virtuel
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dependances...
pip install -q -r requirements.txt

REM Vérifier le fichier .env
if not exist ".env" (
    echo Creation du fichier .env...
    copy .env.example .env
)

REM Vérifier le dossier data
if not exist "data" (
    echo Creation du dossier data...
    mkdir data
)

REM Compter les PDFs
set pdf_count=0
for %%f in (data\*.pdf) do set /a pdf_count+=1
echo [INFO] %pdf_count% fichier(s) PDF trouve(s) dans data/

if %pdf_count%==0 (
    echo [ATTENTION] Aucun PDF trouve. Veuillez ajouter des PDFs dans le dossier data/
)

echo.
echo ==============================================
echo    Lancement de l'application...
echo ==============================================
echo.
echo L'application s'ouvrira dans votre navigateur a:
echo http://localhost:8501
echo.
echo Pour arreter l'application, appuyez sur Ctrl+C
echo.

REM Lancer Streamlit
streamlit run app.py

pause
