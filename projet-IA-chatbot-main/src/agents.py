"""
Agent IA avec outils pour le chatbot ENSAJ
"""
import os
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import AgentAction, AgentFinish

from src.llm_config import llm_config
from src.tools import get_all_tools


# Prompt template pour l'agent ReAct
REACT_PROMPT_TEMPLATE = """Tu es un assistant virtuel intelligent de l'ENSAJ (École Nationale des Sciences Appliquées d'El Jadida).

Tu dois aider les étudiants, professeurs et visiteurs en répondant à leurs questions sur l'école.

Tu as accès aux outils suivants:

{tools}

Utilise le format suivant pour répondre:

Question: la question d'entrée que tu dois répondre
Thought: tu dois toujours réfléchir à ce que tu dois faire
Action: l'action à effectuer, doit être l'un de [{tool_names}]
Action Input: l'entrée pour l'action
Observation: le résultat de l'action
... (ce processus Thought/Action/Action Input/Observation peut se répéter N fois)
Thought: Je connais maintenant la réponse finale
Final Answer: la réponse finale à la question originale

RÈGLES IMPORTANTES:
1. Tu dois TOUJOURS utiliser l'outil "recherche_documents_ensaj" pour toute question nécessitant des informations spécifiques sur l'ENSAJ
2. Base tes réponses UNIQUEMENT sur les informations trouvées dans les documents
3. Si tu ne trouves pas d'information dans les documents, dis-le clairement
4. Ne jamais inventer d'informations
5. Sois précis et cite tes sources quand c'est pertinent
6. Réponds en français de manière claire et professionnelle

Historique de conversation:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""


class ENSAJAgent:
    """Agent conversationnel pour l'ENSAJ avec mémoire et outils"""
    
    def __init__(
        self,
        temperature: float = 0.3,
        max_iterations: int = 5,
        verbose: bool = True
    ):
        self.llm = llm_config.get_llm(temperature=temperature)
        self.tools = get_all_tools()
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # Créer le prompt
        self.prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)
        
        # Créer l'agent ReAct
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Mémoire de conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Agent executor
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Exécute l'agent sur une requête
        
        Args:
            query: Question de l'utilisateur
            
        Returns:
            Dictionnaire avec la réponse et les étapes intermédiaires
        """
        try:
            result = self.agent_executor.invoke({"input": query})
            
            return {
                "success": True,
                "output": result.get("output", "Désolé, je n'ai pas pu générer une réponse."),
                "intermediate_steps": result.get("intermediate_steps", []),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Désolé, une erreur s'est produite: {str(e)}",
                "intermediate_steps": [],
                "error": str(e)
            }
    
    def clear_memory(self):
        """Efface l'historique de conversation"""
        self.memory.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Récupère l'historique de conversation
        
        Returns:
            Liste des messages de conversation
        """
        history = []
        for message in self.memory.chat_memory.messages:
            history.append({
                "role": "human" if message.type == "human" else "ai",
                "content": message.content
            })
        return history


class SimpleRAGChain:
    """Chaîne RAG simple sans agent (alternative plus rapide)"""
    
    def __init__(self, temperature: float = 0.3):
        from langchain.chains import RetrievalQA
        from src.vector_store import vector_store_manager
        
        self.llm = llm_config.get_llm(temperature=temperature)
        self.retriever = vector_store_manager.get_retriever(k=4)
        
        # Template de prompt pour RAG simple
        template = """Tu es un assistant virtuel de l'ENSAJ. Réponds à la question en te basant UNIQUEMENT sur le contexte fourni.

Contexte:
{context}

Question: {question}

Instructions:
- Si la réponse est dans le contexte, réponds de manière claire et précise
- Si la réponse n'est pas dans le contexte, dis "Je ne trouve pas cette information dans les documents disponibles"
- Ne jamais inventer d'informations
- Réponds en français

Réponse:"""
        
        from langchain.prompts import PromptTemplate
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Exécute la chaîne RAG
        
        Args:
            query: Question de l'utilisateur
            
        Returns:
            Dictionnaire avec la réponse et les documents sources
        """
        try:
            result = self.chain.invoke({"query": query})
            
            return {
                "success": True,
                "output": result["result"],
                "source_documents": result.get("source_documents", []),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Désolé, une erreur s'est produite: {str(e)}",
                "source_documents": [],
                "error": str(e)
            }


def create_agent(mode: str = "agent", **kwargs) -> Any:
    """
    Factory pour créer l'agent ou la chaîne RAG
    
    Args:
        mode: "agent" pour l'agent avec outils, "simple" pour RAG simple
        **kwargs: Arguments supplémentaires
        
    Returns:
        Instance d'agent ou de chaîne
    """
    if mode == "agent":
        return ENSAJAgent(**kwargs)
    elif mode == "simple":
        return SimpleRAGChain(**kwargs)
    else:
        raise ValueError(f"Mode inconnu: {mode}. Utilisez 'agent' ou 'simple'")
