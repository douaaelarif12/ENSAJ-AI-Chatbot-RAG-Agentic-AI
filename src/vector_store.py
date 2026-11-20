"""
Gestion de la base vectorielle ChromaDB et traitement des documents PDF
"""
import os
import glob
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from src.llm_config import llm_config


class VectorStoreManager:
    """Gestionnaire de la base vectorielle ChromaDB"""
    
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "ensaj_docs",
        pdf_directory: str = "./data"
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.pdf_directory = pdf_directory
        self.embeddings = llm_config.get_embeddings()
        self.vector_store: Optional[Chroma] = None
        
    def load_pdf_documents(self) -> List[Document]:
        """
        Charge tous les documents PDF du répertoire
        
        Returns:
            Liste des documents chargés
        """
        pdf_files = glob.glob(os.path.join(self.pdf_directory, "*.pdf"))
        
        if not pdf_files:
            print(f"⚠️  Aucun fichier PDF trouvé dans {self.pdf_directory}")
            return []
        
        print(f"📄 Chargement de {len(pdf_files)} fichier(s) PDF...")
        
        documents = []
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(pdf_file)
                docs = loader.load()
                
                # Ajouter des métadonnées
                for doc in docs:
                    doc.metadata['source'] = os.path.basename(pdf_file)
                    doc.metadata['file_path'] = pdf_file
                
                documents.extend(docs)
                print(f"  ✓ {os.path.basename(pdf_file)}: {len(docs)} page(s)")
            except Exception as e:
                print(f"  ✗ Erreur avec {os.path.basename(pdf_file)}: {e}")
        
        print(f"✅ Total: {len(documents)} page(s) chargées")
        return documents
    
    def split_documents(
        self,
        documents: List[Document],
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Document]:
        """
        Découpe les documents en chunks plus petits
        
        Args:
            documents: Liste des documents à découper
            chunk_size: Taille maximale d'un chunk
            chunk_overlap: Chevauchement entre chunks
            
        Returns:
            Liste des chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"📝 Documents découpés en {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, force_recreate: bool = False) -> Chroma:
        """
        Crée ou charge la base vectorielle ChromaDB
        
        Args:
            force_recreate: Force la recréation même si la DB existe
            
        Returns:
            Instance de Chroma
        """
        # Vérifier si la base existe déjà
        db_exists = os.path.exists(self.persist_directory) and os.listdir(self.persist_directory)
        
        if db_exists and not force_recreate:
            print("📦 Chargement de la base vectorielle existante...")
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            print(f"✅ Base vectorielle chargée ({self.vector_store._collection.count()} documents)")
        else:
            print("🔨 Création de la base vectorielle...")
            
            # Charger les PDFs
            documents = self.load_pdf_documents()
            
            if not documents:
                raise ValueError("Aucun document à indexer. Veuillez ajouter des PDFs dans le dossier /data/")
            
            # Découper en chunks
            chunks = self.split_documents(documents)
            
            # Créer la base vectorielle
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
            
            print(f"✅ Base vectorielle créée avec {len(chunks)} chunks")
        
        return self.vector_store
    
    def get_retriever(self, k: int = 4, **kwargs):
        """
        Retourne un retriever pour la recherche sémantique
        
        Args:
            k: Nombre de documents à retourner
            **kwargs: Arguments supplémentaires pour le retriever
            
        Returns:
            Retriever configuré
        """
        if self.vector_store is None:
            self.create_vector_store()
        
        return self.vector_store.as_retriever(
            search_kwargs={"k": k, **kwargs}
        )
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Effectue une recherche de similarité
        
        Args:
            query: Requête de recherche
            k: Nombre de résultats
            
        Returns:
            Liste des documents similaires
        """
        if self.vector_store is None:
            self.create_vector_store()
        
        return self.vector_store.similarity_search(query, k=k)
    
    def add_documents(self, pdf_files: List[str]) -> int:
        """
        Ajoute de nouveaux documents à la base vectorielle
        
        Args:
            pdf_files: Liste des chemins vers les nouveaux PDFs
            
        Returns:
            Nombre de chunks ajoutés
        """
        if self.vector_store is None:
            self.create_vector_store()
        
        documents = []
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(pdf_file)
                docs = loader.load()
                
                for doc in docs:
                    doc.metadata['source'] = os.path.basename(pdf_file)
                    doc.metadata['file_path'] = pdf_file
                
                documents.extend(docs)
            except Exception as e:
                print(f"Erreur avec {pdf_file}: {e}")
        
        if documents:
            chunks = self.split_documents(documents)
            self.vector_store.add_documents(chunks)
            print(f"✅ {len(chunks)} nouveaux chunks ajoutés")
            return len(chunks)
        
        return 0
    
    def reset_database(self):
        """Supprime complètement la base vectorielle"""
        import shutil
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            print("🗑️  Base vectorielle supprimée")
        self.vector_store = None


# Instance globale
vector_store_manager = VectorStoreManager()
