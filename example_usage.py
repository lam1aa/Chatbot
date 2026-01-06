"""
Example usage script for BAföG Chatbot
This demonstrates how to use the chatbot programmatically
"""
import os
from dotenv import load_dotenv
from src.knowledge_base_loader import KnowledgeBaseLoader
from src.rag_chatbot import RAGChatbot


def example_usage():
    """Example of using the chatbot programmatically"""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not found in .env file")
        print("Please create a .env file with your OpenRouter API key")
        print("See .env.example for reference")
        return
    
    print("Loading knowledge base...")
    kb_loader = KnowledgeBaseLoader()
    vectorstore = kb_loader.setup()
    
    print("Initializing chatbot...")
    chatbot = RAGChatbot(vectorstore)
    
    # Example questions
    questions = [
        "Was ist BAföG?",
        "Wer kann BAföG bekommen?",
        "Wie hoch ist die Förderung?",
        "Wann muss ich BAföG zurückzahlen?"
    ]
    
    print("\n=== Example Questions and Answers ===\n")
    
    for question in questions:
        print(f"Frage: {question}")
        result = chatbot.ask(question)
        print(f"Antwort: {result['answer']}\n")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    example_usage()
