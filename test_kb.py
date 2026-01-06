"""
Test script to verify knowledge base loading
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.knowledge_base_loader import KnowledgeBaseLoader


def test_knowledge_base():
    print("=== Testing Knowledge Base Loader ===\n")
    
    # Initialize loader
    kb_loader = KnowledgeBaseLoader(
        knowledge_base_path="./knowledge_base",
        persist_directory="./chroma_db"
    )
    
    # Test document loading
    print("1. Loading documents...")
    documents = kb_loader.load_documents()
    print(f"   ✓ Loaded {len(documents)} documents\n")
    
    # Test document splitting
    print("2. Splitting documents...")
    chunks = kb_loader.split_documents(documents)
    print(f"   ✓ Created {len(chunks)} chunks\n")
    
    # Test vector store creation
    print("3. Creating vector store...")
    vectorstore = kb_loader.create_vector_store(documents)
    print(f"   ✓ Vector store created\n")
    
    # Test similarity search
    print("4. Testing similarity search...")
    query = "Was ist BAföG?"
    results = vectorstore.similarity_search(query, k=2)
    print(f"   Query: '{query}'")
    print(f"   ✓ Found {len(results)} relevant chunks\n")
    
    if results:
        print("   First result preview:")
        print(f"   {results[0].page_content[:200]}...\n")
    
    print("=== All tests passed! ===")
    return True


if __name__ == "__main__":
    try:
        test_knowledge_base()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
