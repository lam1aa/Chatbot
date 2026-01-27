#!/usr/bin/env python3
"""
Flask API Server for BAföG Chatbot
Provides RAG-based responses with source citations
"""
import os
import sys
import time
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
        start_time = time.time()
        
        # Create chatbot instance with provided API key
        chatbot = RAGChatbot(vectorstore, api_key=api_key)
        
        # Get answer with sources
        result = chatbot.ask(question)
        
        # Calculate response time
        response_time = round(time.time() - start_time, 2)
        
        # Check if this is a non-BAföG question response
        is_non_bafog = chatbot._is_non_bafog_response(result['answer'])
        
        # Format sources for response (only if BAföG-related)
        sources = []
        if not is_non_bafog:
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
            'sources': sources,
            'token_usage': result.get('token_usage')
        })
    
    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n🚀 Starting BAföG Chatbot API server on port {port}")
    print(f"   Health check: http://localhost:{port}/health")
    print(f"   Chat endpoint: http://localhost:{port}/chat")
    print(f"   Debug mode: {debug_mode}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
