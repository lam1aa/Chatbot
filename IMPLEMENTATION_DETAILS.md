# Implementation Details

This document describes the current implementation of the BAföG Chatbot.

## Overview

The chatbot has two modes of operation:

1. **Web Version** (Primary) - Browser-based with client-side citations
2. **Python CLI Version** (Advanced) - Local RAG system with ChromaDB

## Web Version Implementation

### How Citations Work Without Backend

The web version provides source citations using client-side keyword matching:

**Files Involved:**
- `index.html` - Web interface
- `app.js` - Application logic and citation system
- `knowledge_base/knowledge_index.json` - Pre-built index of documents with keywords
- `knowledge_base/url_mapping.json` - Maps files to source URLs

**Citation Flow:**
1. On page load, `app.js` fetches `knowledge_index.json`
2. When user asks a question, keywords are extracted
3. Documents are scored based on keyword matches (with English-German mappings)
4. Top 3 relevant sources are selected
5. Sources displayed with clickable URLs

**Keyword Matching:**
- Extracts keywords from user question
- Maps English terms to German equivalents (e.g., "study" → "studium")
- Scores documents based on exact and partial matches
- Prioritizes matches in document names

**Benefits:**
- ✅ No backend server needed
- ✅ Fast response times
- ✅ Works on GitHub Pages
- ✅ Easy to deploy and share

### URL Mapping Generation

**Files:**
- `knowledge_base/URLs.csv` - Source data with file names and URLs
- `generate_url_mapping.py` - Generates JSON mapping
- `knowledge_base/url_mapping.json` - Generated mapping (27 files)

**Process:**
```bash
python generate_url_mapping.py
```

Reads URLs.csv and creates url_mapping.json with filename → URL mappings.

### Knowledge Index Generation

The `knowledge_index.json` file is pre-generated with:
- Document name (formatted)
- File path
- Source URL
- Keywords (extracted from filename and content)

This allows the web version to match questions to relevant sources without requiring a vector database.

## Python CLI Implementation

### RAG Pipeline

**Components:**
- **Document Loader**: `src/knowledge_base_loader.py`
  - Loads .txt files from knowledge_base/
  - Splits into 1000-char chunks with 100-char overlap
  - Creates embeddings using sentence-transformers
  - Stores in ChromaDB

- **Chatbot**: `src/rag_chatbot.py`
  - Retrieves top 3 relevant chunks
  - Generates responses with LangChain
  - Provides source attribution with URLs

**Features:**
- Semantic search (not just keyword matching)
- More accurate retrieval
- Supports custom knowledge bases
- Full control over RAG parameters

### Knowledge Base Management

**Tool**: `kb_manager.py`

Commands:
```bash
python kb_manager.py list      # List documents
python kb_manager.py scrape    # Scrape websites
python kb_manager.py rebuild   # Rebuild vector DB
```

### Web Scraper

**Tool**: `scraper.py`

- Fetches content from URLs
- Cleans HTML (removes scripts, navigation)
- Saves as .txt files
- Updates url_mapping.json
- Respectful scraping with delays

## Optional Backend API

**File**: `api_server.py`

Provides a Flask API endpoint for the web version to use RAG-based retrieval instead of keyword matching.

**Endpoints:**
- `GET /health` - Health check
- `POST /chat` - Chat with RAG retrieval

**Usage:**
```bash
python api_server.py
```

The web interface automatically detects and uses the backend if available, providing more accurate citations through vector search.

## Technology Stack

### Web Version
- HTML/CSS/JavaScript (vanilla)
- OpenRouter API for LLM
- Client-side keyword matching
- GitHub Pages hosting

### Python CLI
- **LLM**: OpenRouter API
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector DB**: ChromaDB (persistent local storage)
- **Framework**: LangChain
- **Web Scraping**: BeautifulSoup4, Requests

### Backend API (Optional)
- **Framework**: Flask
- **CORS**: flask-cors
- **RAG**: Same as Python CLI (ChromaDB + LangChain)

## File Structure

```
├── index.html                    # Web UI
├── app.js                        # Web app + citations
├── styles.css                    # Styling
├── knowledge_base/
│   ├── *.txt                    # Documents
│   ├── knowledge_index.json     # Web citation index
│   ├── url_mapping.json         # URL mappings
│   └── URLs.csv                 # Source data
├── src/
│   ├── knowledge_base_loader.py # Document processing
│   └── rag_chatbot.py           # RAG implementation
├── main.py                      # CLI entry point
├── api_server.py                # Optional backend
├── kb_manager.py                # KB management
├── scraper.py                   # Web scraper
└── generate_url_mapping.py      # Generate mappings
```

## Key Differences: Web vs Python CLI

| Aspect | Web Version | Python CLI |
|--------|-------------|------------|
| **Citation Method** | Keyword matching | Vector similarity |
| **Accuracy** | Good for specific topics | Better for complex queries |
| **Setup** | Just API key | Python environment |
| **Deployment** | Static hosting | Local only |
| **Speed** | Fast (client-side) | Depends on DB size |
| **Customization** | Limited to prompt | Full RAG control |

## Future Enhancements

Potential improvements:
- Hybrid search (keywords + embeddings in web version)
- Multi-language support beyond German
- User feedback on citation relevance
- Improved keyword extraction algorithms
- Caching for backend API responses
