"""
Outils (Tools) pour l'agent IA
"""
from typing import List
from langchain.tools import Tool
from langchain.schema import Document

from src.vector_store import vector_store_manager


def create_document_search_tool() -> Tool:
    """
    Crée un outil de recherche dans les documents ENSAJ
    
    Returns:
        Tool configuré pour la recherche documentaire
    """
    
    def search_documents(query: str) -> str:
        """
        Recherche dans les documents ENSAJ
        
        Args:
            query: La question ou requête de recherche
            
        Returns:
            Contexte pertinent extrait des documents
        """
        try:
            # Recherche dans la base vectorielle
            docs = vector_store_manager.similarity_search(query, k=4)
            
            if not docs:
                return "Aucun document pertinent trouvé dans la base de données ENSAJ."
            
            # Formater les résultats
            context_parts = []
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get('source', 'Source inconnue')
                page = doc.metadata.get('page', '?')
                content = doc.page_content.strip()
                
                context_parts.append(
                    f"[Document {i} - {source} (page {page})]\n{content}\n"
                )
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Erreur lors de la recherche: {str(e)}"
    
    return Tool(
        name="recherche_documents_ensaj",
        description=(
            "Outil pour rechercher des informations dans les documents officiels de l'ENSAJ. "
            "Utilise cet outil pour répondre à des questions sur l'école, les formations, "
            "les règlements, les programmes, etc. "
            "Entrée: une question ou requête de recherche en langage naturel."
        ),
        func=search_documents
    )


def create_calculator_tool() -> Tool:
    """
    Crée un outil de calcul mathématique
    
    Returns:
        Tool configuré pour les calculs
    """
    
    def calculate(expression: str) -> str:
        """
        Évalue une expression mathématique
        
        Args:
            expression: Expression mathématique à évaluer
            
        Returns:
            Résultat du calcul
        """
        try:
            # Nettoyer l'expression
            expression = expression.strip()
            
            # Évaluation sécurisée (attention aux risques de sécurité en production)
            # Pour la production, utilisez une bibliothèque comme numexpr ou sympy
            result = eval(expression, {"__builtins__": {}}, {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "len": len
            })
            
            return f"Le résultat de '{expression}' est: {result}"
            
        except Exception as e:
            return f"Erreur de calcul: {str(e)}. Veuillez vérifier votre expression."
    
    return Tool(
        name="calculatrice",
        description=(
            "Outil pour effectuer des calculs mathématiques. "
            "Utilise cet outil pour résoudre des expressions mathématiques. "
            "Entrée: une expression mathématique (ex: '2 + 2', '10 * 5', '100 / 4')."
        ),
        func=calculate
    )


def create_ensaj_info_tool() -> Tool:
    """
    Crée un outil avec des informations générales sur l'ENSAJ
    
    Returns:
        Tool avec infos statiques ENSAJ
    """
    
    ENSAJ_INFO = {
        "nom": "École Nationale des Sciences Appliquées d'El Jadida",
        "sigle": "ENSAJ",
        "ville": "El Jadida",
        "universite": "Université Chouaib Doukkali",
        "type": "École d'ingénieurs publique",
        "cycles": [
            "Cycle Préparatoire Intégré (2 ans)",
            "Cycle Ingénieur (3 ans)"
        ],
        "filieres": [
            "Génie Informatique",
            "Génie des Systèmes d'Information et de Communication (ISIC)",
            "Génie Électrique",
            "Génie Industriel",
            "Génie Civil"
        ],
        "contact": {
            "adresse": "Route Nationale N°1, Km 7, BP : 1166 El Jadida",
            "telephone": "+212 5 23 39 56 79",
            "email": "contact@ensaj.uca.ma",
            "website": "http://www.ensaj.uca.ma"
        }
    }
    
    def get_ensaj_info(query: str) -> str:
        """
        Retourne des informations générales sur l'ENSAJ
        
        Args:
            query: Type d'information recherchée
            
        Returns:
            Information demandée
        """
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["filière", "formation", "spécialité"]):
            return f"Filières à l'ENSAJ:\n" + "\n".join([f"- {f}" for f in ENSAJ_INFO["filieres"]])
        
        elif any(word in query_lower for word in ["cycle", "durée", "année"]):
            return f"Cycles de formation:\n" + "\n".join([f"- {c}" for c in ENSAJ_INFO["cycles"]])
        
        elif any(word in query_lower for word in ["contact", "adresse", "téléphone", "email"]):
            contact = ENSAJ_INFO["contact"]
            return (
                f"Coordonnées de l'ENSAJ:\n"
                f"Adresse: {contact['adresse']}\n"
                f"Téléphone: {contact['telephone']}\n"
                f"Email: {contact['email']}\n"
                f"Site web: {contact['website']}"
            )
        
        else:
            return (
                f"{ENSAJ_INFO['nom']} ({ENSAJ_INFO['sigle']})\n"
                f"Université: {ENSAJ_INFO['universite']}\n"
                f"Ville: {ENSAJ_INFO['ville']}\n"
                f"Type: {ENSAJ_INFO['type']}\n\n"
                f"Pour plus d'informations spécifiques, utilisez l'outil de recherche documentaire."
            )
    
    return Tool(
        name="info_generale_ensaj",
        description=(
            "Outil pour obtenir des informations générales et statiques sur l'ENSAJ "
            "(nom, localisation, filières, cycles, coordonnées). "
            "Utilise cet outil pour des questions basiques sur l'école. "
            "Pour des informations détaillées, utilise plutôt l'outil de recherche documentaire."
        ),
        func=get_ensaj_info
    )


def get_all_tools() -> List[Tool]:
    """
    Retourne tous les outils disponibles pour l'agent
    
    Returns:
        Liste de tous les outils
    """
    return [
        create_document_search_tool(),
        create_ensaj_info_tool(),
        create_calculator_tool()
    ]
