"""
Test script to verify simplified language instructions in prompts
"""
import sys
import os
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(__file__).parent


def test_python_prompt():
    """Test that Python prompt contains simplified language instructions"""
    print("=== Testing Python Prompt (src/rag_chatbot.py) ===\n")
    
    file_path = SCRIPT_DIR / 'src' / 'rag_chatbot.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for simplified language instructions
    required_phrases = [
        'einfache und leicht verständliche Sprache',
        'Erkläre komplizierte Begriffe in einfachen Worten',
        'Vermeide Fachsprache und schwierige Ausdrücke',
        'kurze, klare Sätze'
    ]
    
    all_found = True
    for phrase in required_phrases:
        if phrase in content:
            print(f"✓ Found: '{phrase}'")
        else:
            print(f"✗ Missing: '{phrase}'")
            all_found = False
    
    if all_found:
        print("\n✅ All simplified language instructions found in Python prompt!\n")
    else:
        print("\n❌ Some instructions missing from Python prompt!\n")
        sys.exit(1)
    
    return all_found


def test_javascript_prompt():
    """Test that JavaScript prompt contains simplified language instructions"""
    print("=== Testing JavaScript Prompt (app.js) ===\n")
    
    file_path = SCRIPT_DIR / 'app.js'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for simplified language instructions
    required_phrases = [
        'Use simple and easy-to-understand language',
        'Explain complex terms in simple words',
        'Avoid technical jargon and complicated expressions',
        'Use short, clear sentences'
    ]
    
    all_found = True
    for phrase in required_phrases:
        if phrase in content:
            print(f"✓ Found: '{phrase}'")
        else:
            print(f"✗ Missing: '{phrase}'")
            all_found = False
    
    if all_found:
        print("\n✅ All simplified language instructions found in JavaScript prompt!\n")
    else:
        print("\n❌ Some instructions missing from JavaScript prompt!\n")
        sys.exit(1)
    
    return all_found


def test_flowchart_documentation():
    """Test that flowchart documentation was added"""
    print("=== Testing Flowchart Documentation (IMPLEMENTATION_DETAILS.md) ===\n")
    
    file_path = SCRIPT_DIR / 'IMPLEMENTATION_DETAILS.md'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for flowchart sections
    required_sections = [
        'System Architecture Flowchart',
        'Knowledge Base Construction Flow',
        'Web Version User Interaction Flow',
        'Python CLI Version RAG Flow',
        'Artefact Design Details',
        'Language Simplification Feature'
    ]
    
    all_found = True
    for section in required_sections:
        if section in content:
            print(f"✓ Found section: '{section}'")
        else:
            print(f"✗ Missing section: '{section}'")
            all_found = False
    
    # Check for specific flowchart elements
    flowchart_elements = [
        'ChromaDB',
        'OpenRouter',
        'knowledge_index.json',
        'url_mapping.json',
        'Keyword Extraction',
        'Semantic search'
    ]
    
    print("\nFlowchart elements:")
    for element in flowchart_elements:
        if element in content:
            print(f"✓ Found element: '{element}'")
        else:
            print(f"✗ Missing element: '{element}'")
            all_found = False
    
    if all_found:
        print("\n✅ All flowchart documentation found!\n")
    else:
        print("\n❌ Some flowchart documentation missing!\n")
        sys.exit(1)
    
    return all_found


if __name__ == "__main__":
    try:
        # Test all components
        test_python_prompt()
        test_javascript_prompt()
        test_flowchart_documentation()
        
        print("\n" + "="*70)
        print("🎉 All simplified language and flowchart tests passed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
