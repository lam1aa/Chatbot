# Implementation Details

This document describes how the three requirements from the problem statement have been implemented.

## Requirements Summary

1. **Use English language for the Chatbot UI**
2. **Check URLs.csv and create URL mapping for TXT files**
3. **Provide citation of info sources through URL mapping**

## Implementation

### 1. English Language UI ✅

**Changes Made:**
- `index.html`: Translated all German text to English
  - "Dein Assistent für BAföG-Fragen" → "Your Assistant for BAföG Questions"
  - "API-Schlüssel erforderlich" → "API Key Required"
  - "Speichern" → "Save"
  - "Chat löschen" → "Clear Chat"
  - "Stelle deine Frage" → "Ask your question"
  - "Open Source auf GitHub" → "Open Source on GitHub"
  
- `app.js`: Translated all UI messages to English
  - Alert messages
  - Error messages
  - Welcome message
  - Confirmation dialogs
  - System prompts (now in English)

**Files Modified:**
- `index.html`
- `app.js`

### 2. URL Mapping from URLs.csv ✅

**Implementation:**
- Created `generate_url_mapping.py` script that:
  - Reads `knowledge_base/URLs.csv`
  - Parses CSV entries with columns: file_name, url, doc_type
  - Filters only TXT file entries (doc_type == 'TXT')
  - Generates `knowledge_base/url_mapping.json` with filename → URL mappings

**Generated Mapping:**
- 27 TXT files mapped to their source URLs
- JSON format for easy consumption by both Python and JavaScript
- Example mapping:
  ```json
  {
    "Antragsformulare.txt": "https://www.xn--bafg-7qa.de/...",
    "Fragen_und_Antworten.txt": "https://www.xn--bafg-7qa.de/...",
    ...
  }
  ```

**Files Created:**
- `generate_url_mapping.py` - Script to generate mappings
- `knowledge_base/url_mapping.json` - Generated mapping file (27 entries)

### 3. Source Citations with URLs ✅

**Implementation Approach:**
We implemented a two-tier system to support citations:

#### Option A: Backend API with Full RAG (Recommended)
- Created `api_server.py` - Flask-based API server
- Uses existing RAG chatbot (`src/rag_chatbot.py`) to retrieve relevant documents
- Returns responses with actual source citations based on vector similarity
- Citations include:
  - Document name (formatted)
  - Source URL from url_mapping.json
  - Original filename

**How it works:**
1. Backend loads knowledge base and URL mapping
2. User asks question via web interface
3. Backend performs RAG retrieval to find relevant documents
4. Returns answer with sources that actually contributed to the response
5. Web UI displays sources with clickable URLs

**Files Created:**
- `api_server.py` - Backend API server
- Updated `app.js` to support backend API calls
- Updated `requirements.txt` to include Flask dependencies

#### Option B: Direct OpenRouter (Fallback)
- When backend is not running, web app makes direct API calls to OpenRouter
- No source citations (as no RAG retrieval happens)
- Provides basic chatbot functionality

**Files Modified:**
- `app.js` - Added backend detection and dual-mode support
- `styles.css` - Added styling for source citations

### Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (index.html)  │
└────────┬────────┘
         │
         ├─── Option A (with backend) ───┐
         │                               │
         │                      ┌────────▼─────────┐
         │                      │   api_server.py  │
         │                      │   (Flask API)    │
         │                      └────────┬─────────┘
         │                               │
         │                      ┌────────▼─────────┐
         │                      │  RAG Chatbot     │
         │                      │  + ChromaDB      │
         │                      │  + URL Mapping   │
         │                      └──────────────────┘
         │
         └─── Option B (no backend) ──────────────┐
                                                   │
                                          ┌────────▼────────┐
                                          │   OpenRouter    │
                                          │   (Direct API)  │
                                          └─────────────────┘
```

### How to Use

#### With Source Citations (Full Implementation):
1. Run: `python generate_url_mapping.py` (already done, url_mapping.json exists)
2. Run: `python api_server.py` (starts backend on port 5000)
3. Open `index.html` in browser
4. Enter OpenRouter API key
5. Ask questions and get responses with source citations!

#### Without Backend (Basic Mode):
1. Open `index.html` in browser (or visit GitHub Pages)
2. Enter OpenRouter API key
3. Ask questions (no source citations, but functional)

### Files Summary

**New Files:**
- `generate_url_mapping.py` - Generates URL mapping from CSV
- `api_server.py` - Backend API for RAG with citations
- `IMPLEMENTATION_DETAILS.md` - This document

**Modified Files:**
- `index.html` - English UI
- `app.js` - English messages + backend support + citation display
- `styles.css` - Citation styling
- `requirements.txt` - Added Flask dependencies
- `README.md` - Updated documentation
- `knowledge_base/url_mapping.json` - Generated from URLs.csv (27 entries)

### Testing

All three requirements have been verified:
1. ✅ UI is fully in English (screenshot available)
2. ✅ URL mapping generated with 27 TXT file mappings
3. ✅ Backend API supports source citations with URLs
4. ✅ Web UI displays citations when backend is available
5. ✅ Graceful fallback when backend is unavailable

### Future Enhancements

If desired, the implementation could be further enhanced by:
- Adding caching for backend responses
- Implementing user feedback on source relevance
- Adding more detailed citation information (page numbers, sections)
- Supporting multiple languages dynamically
