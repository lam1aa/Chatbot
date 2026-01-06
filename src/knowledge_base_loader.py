"""
Knowledge Base Loader
Loads and processes BAföG text files into a vector database
"""
import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class KnowledgeBaseLoader:
    def __init__(self, knowledge_base_path="./knowledge_base", persist_directory="./chroma_db"):
        self.knowledge_base_path = knowledge_base_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
    def load_documents(self):
        """Load all text documents from knowledge base directory"""
        print(f"Loading documents from {self.knowledge_base_path}...")
        
        loader = DirectoryLoader(
            self.knowledge_base_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        documents = loader.load()
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents):
        """Split documents into smaller chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, documents):
        """Create or load vector store from documents"""
        if os.path.exists(self.persist_directory):
            print("Loading existing vector store...")
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            print("Creating new vector store...")
            chunks = self.split_documents(documents)
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            print("Vector store created and persisted")
        
        return vectorstore
    
    def setup(self):
        """Setup the knowledge base"""
        documents = self.load_documents()
        vectorstore = self.create_vector_store(documents)
        return vectorstore
