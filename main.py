"""
Main entry point for BAföG RAG Chatbot
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from src.knowledge_base_loader import KnowledgeBaseLoader
from src.rag_chatbot import RAGChatbot


def main():
    print("Initializing BAföG Chatbot...")
    
    # Load knowledge base
    kb_loader = KnowledgeBaseLoader(
        knowledge_base_path="./knowledge_base",
        persist_directory="./chroma_db"
    )
    
    try:
        vectorstore = kb_loader.setup()
        print("Knowledge base loaded successfully!\n")
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        print("\nMake sure you have .txt files in the knowledge_base/ directory")
        return
    
    # Initialize chatbot
    try:
        chatbot = RAGChatbot(vectorstore)
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please create a .env file with your OPENROUTER_API_KEY")
        print("See .env.example for reference")
        return
    
    # Start chat
    chatbot.chat()


if __name__ == "__main__":
    main()
