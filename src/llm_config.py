"""
Configuration des modèles LLM et Embeddings avec Ollama
"""
import os
from typing import Optional
from langchain_ollama import OllamaLLM, OllamaEmbeddings


class LLMConfig:
    """Configuration centralisée pour les modèles Ollama"""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        llm_model: Optional[str] = None,
        embed_model: Optional[str] = None
    ):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm_model = llm_model or os.getenv("OLLAMA_LLM_MODEL", "gemma2:2b")
        self.embed_model = embed_model or os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text:latest")
    
    def get_llm(self, temperature: float = 0.7, **kwargs) -> OllamaLLM:
        """
        Initialise et retourne le modèle LLM Ollama
        
        Args:
            temperature: Température pour la génération (0.0 = déterministe, 1.0 = créatif)
            **kwargs: Arguments supplémentaires pour OllamaLLM
            
        Returns:
            Instance configurée d'OllamaLLM
        """
        return OllamaLLM(
            base_url=self.base_url,
            model=self.llm_model,
            temperature=temperature,
            **kwargs
        )
    
    def get_embeddings(self, **kwargs) -> OllamaEmbeddings:
        """
        Initialise et retourne le modèle d'embeddings Ollama
        
        Args:
            **kwargs: Arguments supplémentaires pour OllamaEmbeddings
            
        Returns:
            Instance configurée d'OllamaEmbeddings
        """
        return OllamaEmbeddings(
            base_url=self.base_url,
            model=self.embed_model,
            **kwargs
        )
    
    def test_connection(self) -> bool:
        """
        Teste la connexion avec Ollama
        
        Returns:
            True si la connexion est OK, False sinon
        """
        try:
            import ollama
            # Test de connexion basique
            ollama.list()
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion Ollama: {e}")
            return False
    
    def list_models(self) -> list:
        """
        Liste tous les modèles disponibles dans Ollama
        
        Returns:
            Liste des modèles disponibles
        """
        try:
            import ollama
            models = ollama.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des modèles: {e}")
            return []


# Instance globale pour faciliter l'usage
llm_config = LLMConfig()
