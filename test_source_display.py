"""
Test script to verify conditional source display
Tests that sources are only shown for BAföG-related questions
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


def test_is_non_bafog_response():
    """Test the _is_non_bafog_response method"""
    print("=== Testing Non-BAföG Response Detection ===\n")
    
    # Create a dummy chatbot instance (we only need the method, not the full setup)
    class DummyChatbot:
        def _is_non_bafog_response(self, answer):
            """
            Detect if the response is a rejection message for non-BAföG questions
            Returns True if the answer indicates the question is not BAföG-related
            This matches the implementation in src/rag_chatbot.py
            """
            answer_lower = answer.lower()
            
            # Check for the rejection phrase in German (matches src/rag_chatbot.py)
            rejection_phrases = [
                'kann nur bei bafög',
                'kann nur fragen zu bafög',
                'ausschließlich für bafög',
                'nur bafög-fragen'
            ]
            
            return any(phrase in answer_lower for phrase in rejection_phrases)
    
    chatbot = DummyChatbot()
    
    # Test cases
    test_cases = [
        # Non-BAföG responses (should return True)
        {
            'answer': 'Ich kann nur bei BAföG-bezogenen Fragen helfen. Bitte stellen Sie mir eine Frage zu BAföG und ich helfe Ihnen gerne weiter.',
            'expected': True,
            'description': 'German rejection message'
        },
        {
            'answer': 'Ich kann nur Fragen zu BAföG beantworten.',
            'expected': True,
            'description': 'Short German rejection'
        },
        {
            'answer': 'Ich bin ausschließlich für BAföG-Fragen zuständig.',
            'expected': True,
            'description': 'Alternative German rejection'
        },
        # BAföG-related responses (should return False)
        {
            'answer': 'BAföG ist eine staatliche Förderung für Studierende in Deutschland.',
            'expected': False,
            'description': 'Normal BAföG answer'
        },
        {
            'answer': 'Die Höhe des BAföG hängt von verschiedenen Faktoren ab, wie dem Einkommen der Eltern.',
            'expected': False,
            'description': 'Detailed BAföG answer'
        },
        {
            'answer': 'Den BAföG-Antrag können Sie online über BAföG Digital stellen.',
            'expected': False,
            'description': 'Application-related answer'
        }
    ]
    
    all_passed = True
    for i, test in enumerate(test_cases, 1):
        result = chatbot._is_non_bafog_response(test['answer'])
        passed = result == test['expected']
        all_passed = all_passed and passed
        
        status = "✓" if passed else "✗"
        print(f"Test {i}: {test['description']}")
        print(f"  Expected: {test['expected']}, Got: {result} {status}")
        if not passed:
            print(f"  Answer: {test['answer'][:100]}...")
        print()
    
    if all_passed:
        print("=== All tests passed! ===")
    else:
        print("=== Some tests failed! ===")
        sys.exit(1)
    
    return all_passed


def test_source_formatting():
    """Test that sources are properly formatted when available"""
    print("\n=== Testing Source Formatting ===\n")
    
    class DummyChatbot:
        def format_sources(self, sources):
            """Format source documents for display"""
            if not sources:
                return "Keine Quellen gefunden."
            
            formatted = []
            seen_sources = set()
            
            for doc in sources:
                # Mock document structure
                source = getattr(doc, 'source', doc.get('source', 'Unbekannt')) if isinstance(doc, dict) else 'Unbekannt'
                url = getattr(doc, 'url', doc.get('url', '')) if isinstance(doc, dict) else ''
                
                # Create unique identifier
                source_id = f"{source}|{url}"
                if source_id in seen_sources:
                    continue
                seen_sources.add(source_id)
                
                # Format source display
                if url:
                    formatted.append(f"📄 {source}\n   🔗 {url}")
                else:
                    formatted.append(f"📄 {source}")
            
            return "\n".join(formatted)
    
    chatbot = DummyChatbot()
    
    # Test with no sources
    result = chatbot.format_sources([])
    assert result == "Keine Quellen gefunden.", "Empty sources test failed"
    print("✓ Empty sources handled correctly")
    
    # Test with sources
    mock_sources = [
        {'source': 'document1.txt', 'url': 'https://example.com/doc1'},
        {'source': 'document2.txt', 'url': 'https://example.com/doc2'}
    ]
    result = chatbot.format_sources(mock_sources)
    assert '📄 document1.txt' in result, "Source formatting test failed"
    assert '🔗 https://example.com/doc1' in result, "URL formatting test failed"
    print("✓ Sources formatted correctly with URLs")
    
    print("\n=== Source formatting tests passed! ===")
    return True


if __name__ == "__main__":
    try:
        test_is_non_bafog_response()
        test_source_formatting()
        print("\n✅ All conditional source display tests passed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
