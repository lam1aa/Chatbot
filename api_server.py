#!/usr/bin/env python3
"""
Flask API Server for BAföG Chatbot
Provides RAG-based responses with source citations
"""
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from src.knowledge_base_loader import KnowledgeBaseLoader
from src.rag_chatbot import RAGChatbot

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for browser access

# Initialize knowledge base and chatbot
print("Initializing knowledge base...")
kb_loader = KnowledgeBaseLoader(
    knowledge_base_path="./knowledge_base",
    persist_directory="./chroma_db"
)

try:
    vectorstore = kb_loader.setup()
    print("Knowledge base loaded successfully!")
except Exception as e:
    print(f"Error loading knowledge base: {e}")
    vectorstore = None

# Global chatbot instance (will be initialized per request with API key)
chatbot = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'knowledge_base_loaded': vectorstore is not None
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint that returns responses with source citations"""
    if vectorstore is None:
        return jsonify({
            'error': 'Knowledge base not loaded'
        }), 500
    
    data = request.json
    question = data.get('question')
    api_key = data.get('api_key')
    
    if not question:
        return jsonify({
            'error': 'No question provided'
        }), 400
    
    if not api_key:
        return jsonify({
            'error': 'No API key provided'
        }), 400
    
    try:
        # Create chatbot instance with provided API key
        chatbot = RAGChatbot(vectorstore, api_key=api_key)
        
        # Get answer with sources
        result = chatbot.ask(question)
        
        # Format sources for response
        sources = []
        seen_sources = set()
        
        for doc in result['sources']:
            source_file = os.path.basename(doc.metadata.get('source', 'Unknown'))
            url = doc.metadata.get('url', '')
            
            # Create unique identifier
            source_id = f"{source_file}|{url}"
            if source_id in seen_sources:
                continue
            seen_sources.add(source_id)
            
            if url:
                sources.append({
                    'name': source_file.replace('.txt', '').replace('-', ' ').title(),
                    'url': url,
                    'file': source_file
                })
        
        return jsonify({
            'answer': result['answer'],
            'sources': sources
        })
    
    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n🚀 Starting BAföG Chatbot API server on port {port}")
    print(f"   Health check: http://localhost:{port}/health")
    print(f"   Chat endpoint: http://localhost:{port}/chat")
    app.run(host='0.0.0.0', port=port, debug=True)
