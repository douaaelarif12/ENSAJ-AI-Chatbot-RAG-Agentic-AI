"""
Chatbot ENSAJ - Application Streamlit avec RAG et Agentic AI
"""
import os
import sys
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from src.llm_config import llm_config
from src.vector_store import vector_store_manager
from src.agents import create_agent


# Configuration de la page
st.set_page_config(
    page_title="Chatbot ENSAJ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .source-doc {
        background-color: #E0F2FE;
        border-left: 3px solid #0EA5E9;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .tool-usage {
        background-color: #FEF3C7;
        border-left: 3px solid #F59E0B;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialise les variables de session"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
    
    if "vector_store_loaded" not in st.session_state:
        st.session_state.vector_store_loaded = False
    
    if "show_intermediate_steps" not in st.session_state:
        st.session_state.show_intermediate_steps = True


def load_vector_store():
    """Charge ou crée la base vectorielle"""
    with st.spinner("🔄 Chargement de la base de données..."):
        try:
            vector_store_manager.create_vector_store()
            st.session_state.vector_store_loaded = True
            return True
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement de la base vectorielle: {e}")
            return False


def initialize_agent(mode: str, temperature: float):
    """Initialise l'agent IA"""
    try:
        st.session_state.agent = create_agent(
            mode=mode,
            temperature=temperature,
            verbose=True
        )
        return True
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation de l'agent: {e}")
        return False


def display_sidebar():
    """Affiche la barre latérale avec les paramètres"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Test de connexion Ollama
        st.markdown("### 🔌 Connexion Ollama")
        if st.button("Tester la connexion"):
            if llm_config.test_connection():
                st.success("✅ Connexion OK")
                models = llm_config.list_models()
                if models:
                    st.info(f"Modèles disponibles: {', '.join(models)}")
            else:
                st.error("❌ Connexion échouée")
        
        st.markdown("---")
        
        # Mode de l'agent
        st.markdown("### 🤖 Mode de l'agent")
        mode = st.radio(
            "Sélectionnez le mode:",
            ["agent", "simple"],
            format_func=lambda x: {
                "agent": "🧠 Agent avec outils (recommandé)",
                "simple": "⚡ RAG simple (plus rapide)"
            }[x],
            help="Mode 'agent': utilise des outils et raisonne. Mode 'simple': recherche directe."
        )
        
        # Température
        st.markdown("### 🌡️ Température")
        temperature = st.slider(
            "Créativité du modèle:",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="0 = déterministe, 1 = créatif"
        )
        
        # Options d'affichage
        st.markdown("### 👁️ Affichage")
        show_steps = st.checkbox(
            "Montrer les étapes de raisonnement",
            value=st.session_state.show_intermediate_steps,
            help="Affiche comment l'agent utilise les outils"
        )
        st.session_state.show_intermediate_steps = show_steps
        
        st.markdown("---")
        
        # Gestion de la base vectorielle
        st.markdown("### 📚 Base de données")
        
        if st.session_state.vector_store_loaded:
            st.success("✅ Base vectorielle chargée")
            
            if st.button("🔄 Recharger la base"):
                vector_store_manager.reset_database()
                st.session_state.vector_store_loaded = False
                st.rerun()
        else:
            if st.button("📦 Charger la base"):
                if load_vector_store():
                    st.success("Base chargée!")
                    st.rerun()
        
        st.markdown("---")
        
        # Actions
        st.markdown("### 🔧 Actions")
        
        if st.button("🗑️ Effacer la conversation"):
            st.session_state.messages = []
            if st.session_state.agent and hasattr(st.session_state.agent, 'clear_memory'):
                st.session_state.agent.clear_memory()
            st.rerun()
        
        if st.button("🔄 Réinitialiser l'agent"):
            st.session_state.agent = None
            if initialize_agent(mode, temperature):
                st.success("Agent réinitialisé!")
                st.rerun()
        
        st.markdown("---")
        
        # Informations
        st.markdown("### ℹ️ Informations")
        st.info(f"""
        **Modèle LLM:** {llm_config.llm_model}  
        **Modèle Embeddings:** {llm_config.embed_model}  
        **URL Ollama:** {llm_config.base_url}
        """)
        
        return mode, temperature


def display_intermediate_steps(steps):
    """Affiche les étapes intermédiaires de l'agent"""
    if not steps or not st.session_state.show_intermediate_steps:
        return
    
    with st.expander("🔍 Étapes de raisonnement", expanded=False):
        for i, (action, observation) in enumerate(steps, 1):
            st.markdown(f"**Étape {i}:**")
            st.markdown(f'<div class="tool-usage">🛠️ <strong>Outil:</strong> {action.tool}<br>📝 <strong>Entrée:</strong> {action.tool_input}</div>', unsafe_allow_html=True)
            st.markdown(f"**Observation:** {observation[:500]}..." if len(observation) > 500 else f"**Observation:** {observation}")
            st.markdown("---")


def display_sources(source_docs):
    """Affiche les sources utilisées"""
    if not source_docs:
        return
    
    with st.expander("📄 Sources utilisées", expanded=False):
        for i, doc in enumerate(source_docs, 1):
            source = doc.metadata.get('source', 'Source inconnue')
            page = doc.metadata.get('page', '?')
            st.markdown(
                f'<div class="source-doc">'
                f'<strong>Document {i}:</strong> {source} (page {page})<br>'
                f'{doc.page_content[:300]}...'
                f'</div>',
                unsafe_allow_html=True
            )


def main():
    """Fonction principale de l'application"""
    
    # Initialiser l'état de session
    initialize_session_state()
    
    # En-tête
    st.markdown('<div class="main-header">🎓 Chatbot ENSAJ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Assistant virtuel intelligent avec RAG et Agentic AI</div>', unsafe_allow_html=True)
    
    # Barre latérale
    mode, temperature = display_sidebar()
    
    # Vérifier que la base vectorielle est chargée
    if not st.session_state.vector_store_loaded:
        st.warning("⚠️ La base de données n'est pas encore chargée. Veuillez cliquer sur 'Charger la base' dans la barre latérale.")
        
        # Tentative de chargement automatique
        if st.button("📦 Charger automatiquement la base"):
            if load_vector_store():
                st.rerun()
        return
    
    # Initialiser l'agent si nécessaire
    if st.session_state.agent is None:
        with st.spinner("🤖 Initialisation de l'agent..."):
            if not initialize_agent(mode, temperature):
                st.error("Impossible d'initialiser l'agent. Vérifiez que Ollama est lancé.")
                return
    
    # Afficher l'historique de conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Afficher les étapes si disponibles
            if "intermediate_steps" in message:
                display_intermediate_steps(message["intermediate_steps"])
            
            # Afficher les sources si disponibles
            if "source_documents" in message:
                display_sources(message["source_documents"])
    
    # Input utilisateur
    if prompt := st.chat_input("Posez votre question sur l'ENSAJ..."):
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Générer la réponse
        with st.chat_message("assistant"):
            with st.spinner("🤔 Réflexion en cours..."):
                result = st.session_state.agent.run(prompt)
                
                if result["success"]:
                    response = result["output"]
                    st.markdown(response)
                    
                    # Préparer le message à sauvegarder
                    assistant_message = {
                        "role": "assistant",
                        "content": response
                    }
                    
                    # Ajouter les étapes intermédiaires si disponibles
                    if "intermediate_steps" in result and result["intermediate_steps"]:
                        assistant_message["intermediate_steps"] = result["intermediate_steps"]
                        display_intermediate_steps(result["intermediate_steps"])
                    
                    # Ajouter les sources si disponibles
                    if "source_documents" in result and result["source_documents"]:
                        assistant_message["source_documents"] = result["source_documents"]
                        display_sources(result["source_documents"])
                    
                    st.session_state.messages.append(assistant_message)
                else:
                    error_msg = f"❌ Erreur: {result['error']}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


if __name__ == "__main__":
    main()
