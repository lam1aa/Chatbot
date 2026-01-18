# Implementation Details

This document describes the current implementation of the BAföG Chatbot.

## Overview

The chatbot has two modes of operation:

1. **Web Version** (Primary) - Browser-based with client-side citations
2. **Python CLI Version** (Advanced) - Local RAG system with ChromaDB

## System Architecture Flowchart

### High-Level System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BAföG Chatbot System                        │
│                                                                       │
│  ┌──────────────────────┐              ┌──────────────────────┐    │
│  │   Web Version        │              │  Python CLI Version  │    │
│  │  (Browser-based)     │              │   (Local RAG)        │    │
│  └──────────────────────┘              └──────────────────────┘    │
│           │                                       │                  │
│           ├───────────────┬───────────────────────┤                 │
│           │               │                       │                  │
│           ▼               ▼                       ▼                  │
│  ┌─────────────┐  ┌─────────────┐      ┌─────────────────┐        │
│  │ Knowledge   │  │  OpenRouter │      │   ChromaDB      │        │
│  │ Index JSON  │  │  LLM API    │      │  Vector Store   │        │
│  └─────────────┘  └─────────────┘      └─────────────────┘        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Knowledge Base Construction Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│              Knowledge Base Construction Process                     │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Data Collection
┌────────────────────┐
│  Source Content    │
│  - Web Scraping    │──────┐
│  - Manual Docs     │      │
│  - BAföG Website   │      │
└────────────────────┘      │
                            ▼
                   ┌────────────────────┐
                   │  .txt Files        │
                   │  (knowledge_base/) │
                   │  - 27+ documents   │
                   └────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
Step 2: Artefact Creation

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ URL Mapping     │  │ Knowledge Index │  │ Vector Database │
│ (url_mapping.   │  │ (knowledge_     │  │ (ChromaDB)      │
│  json)          │  │  index.json)    │  │                 │
│                 │  │                 │  │                 │
│ Purpose:        │  │ Purpose:        │  │ Purpose:        │
│ - Map files to  │  │ - Keyword-based │  │ - Semantic      │
│   source URLs   │  │   matching      │  │   search        │
│ - Citation      │  │ - Client-side   │  │ - Embeddings    │
│   links         │  │   citations     │  │ - Python CLI    │
│                 │  │ - Web version   │  │                 │
│ Used by:        │  │                 │  │ Used by:        │
│ - Web + CLI     │  │ Used by:        │  │ - CLI only      │
│                 │  │ - Web only      │  │ - Optional API  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Web Version User Interaction Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Web Version User Flow                             │
└─────────────────────────────────────────────────────────────────────┘

1. Page Load
   │
   ├──▶ Load knowledge_index.json (26+ documents)
   │
   └──▶ Check for backend API (optional)

2. User Input
   │
   └──▶ User enters question
        │
        ▼
3. Keyword Extraction
   │
   ├──▶ Extract keywords from question
   │
   ├──▶ Apply English-German mapping
   │
   └──▶ Score documents by keyword match
        │
        ▼
4. LLM Processing
   │
   ├──▶ Build conversation history
   │
   ├──▶ Add system prompt (simplified language)
   │
   └──▶ Call OpenRouter API
        │
        ▼
5. Response Generation
   │
   ├──▶ Receive answer from LLM
   │
   ├──▶ Match top 3 relevant sources
   │
   └──▶ Display answer + citations with URLs
        │
        ▼
6. Display to User
   │
   └──▶ Show response in chat interface
```

### Python CLI Version RAG Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Python CLI RAG Pipeline                            │
└─────────────────────────────────────────────────────────────────────┘

1. Initialization
   │
   ├──▶ Load .txt files from knowledge_base/
   │
   ├──▶ Load url_mapping.json
   │
   └──▶ Check for existing ChromaDB
        │
        ▼
2. Document Processing (if rebuilding)
   │
   ├──▶ Split documents into chunks
   │    (1000 chars, 100 overlap)
   │
   ├──▶ Generate embeddings
   │    (all-MiniLM-L6-v2)
   │
   └──▶ Store in ChromaDB with metadata
        │
        ▼
3. User Query
   │
   └──▶ User enters question
        │
        ▼
4. Retrieval
   │
   ├──▶ Embed question
   │
   ├──▶ Semantic search in ChromaDB
   │
   └──▶ Retrieve top 3 similar chunks
        │
        ▼
5. Generation
   │
   ├──▶ Build prompt with context
   │
   ├──▶ Add simplified language instruction
   │
   └──▶ Call OpenRouter API via LangChain
        │
        ▼
6. Response
   │
   ├──▶ Generate answer
   │
   ├──▶ Extract source documents
   │
   ├──▶ Add URL citations
   │
   └──▶ Display to user
```

### Artefact Design Details

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Artefact Design                              │
└─────────────────────────────────────────────────────────────────────┘

1. url_mapping.json
   ┌────────────────────────────────────────┐
   │ {                                      │
   │   "filename.txt": "https://url.de",   │
   │   ...                                  │
   │ }                                      │
   └────────────────────────────────────────┘
   Purpose: Link documents to original sources
   Generation: generate_url_mapping.py
   Used by: Both Web and CLI versions

2. knowledge_index.json
   ┌────────────────────────────────────────┐
   │ [                                      │
   │   {                                    │
   │     "name": "Document Name",           │
   │     "file": "path/to/file.txt",        │
   │     "url": "https://source.url",       │
   │     "keywords": ["keyword1", ...]      │
   │   }                                    │
   │ ]                                      │
   └────────────────────────────────────────┘
   Purpose: Enable client-side citations
   Generation: create_knowledge_index.py
   Used by: Web version only

3. ChromaDB Vector Store
   ┌────────────────────────────────────────┐
   │ Document Chunks + Embeddings           │
   │ - Text content                         │
   │ - Vector embeddings (384 dimensions)   │
   │ - Metadata (source, url)               │
   └────────────────────────────────────────┘
   Purpose: Semantic search and retrieval
   Generation: knowledge_base_loader.py
   Used by: CLI and optional backend API

4. Language Simplification Feature
   ┌────────────────────────────────────────┐
   │ System Prompt Instructions:            │
   │ - Use simple language                  │
   │ - Explain complex terms                │
   │ - Avoid jargon                         │
   │ - Short, clear sentences               │
   └────────────────────────────────────────┘
   Implementation: 
   - src/rag_chatbot.py (Python)
   - app.js (Web)
```

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

### Why the Website Cannot Use Vector Database Directly

The web version uses keyword matching instead of a vector database for several technical reasons:

**1. Browser Limitations:**
- Vector databases like ChromaDB require Python runtime and cannot run in browsers
- Browsers only support JavaScript, HTML, and CSS
- No access to file system or persistent database storage
- Cannot install Python packages or run native code

**2. Embedding Model Size:**
- The embedding model (all-MiniLM-L6-v2) is ~80-90 MB
- Would need to download and run in browser using TensorFlow.js or ONNX
- Slow initial load time and high memory usage
- Not practical for mobile devices with limited resources

**3. Vector Store Size:**
- ChromaDB vector store contains embeddings for all document chunks
- Would be several megabytes of data to download
- Requires computational resources to perform similarity search
- Not efficient for static website hosting

**4. Deployment Constraints:**
- GitHub Pages only supports static files (HTML, CSS, JS, JSON)
- Cannot run server-side code or databases
- No Python runtime available
- Maximum simplicity and accessibility is the goal

**Alternative Solutions:**

The chatbot provides two options to work around these limitations:

**Option 1: Client-Side Keyword Matching (Default)**
- Lightweight JSON index (~50 KB)
- Fast keyword-based document matching
- Works entirely in browser
- Good enough for most BAföG queries
- ✅ Currently implemented

**Option 2: Optional Backend API Server**
- Run `api_server.py` on a separate server
- Provides full RAG with vector search
- Web interface auto-detects and uses if available
- More accurate but requires server infrastructure
- ⚠️ Optional, not required for basic functionality

**Future Possibilities:**
- **WebAssembly (WASM)**: Could potentially run embedding models in browser, but still large download
- **Serverless Functions**: Deploy vector search as cloud function (AWS Lambda, Vercel, etc.)
- **Hybrid Approach**: Combine keyword matching with cloud-based semantic search
- **Browser-Native Embeddings**: Wait for browser APIs to support ML models natively

**Current Design Decision:**
The website prioritizes **accessibility and ease of deployment** over perfect accuracy. Keyword matching provides good-enough results for most questions while enabling:
- Zero server costs
- Instant deployment via GitHub Pages  
- Works on any device with a browser
- No maintenance or infrastructure required

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
| **Vector Database** | ❌ Not possible (browser limitation) | ✅ Yes (ChromaDB) |
| **Embedding Model** | ❌ Too large for browser (~90 MB) | ✅ Yes (all-MiniLM-L6-v2) |
| **Runtime** | JavaScript in browser | Python on local machine |
| **Knowledge Base** | JSON index (~50 KB) | Vector embeddings (several MB) |
| **Server Required** | ❌ No (works on GitHub Pages) | N/A (runs locally) |
| **Hosting Cost** | Free | N/A |

**Why These Differences Exist:**

The web version is designed to be **statically hosted** (no server), which means:
- Cannot run Python code or databases
- Cannot use vector embeddings (too large and computationally intensive)
- Must rely on lightweight JavaScript-based keyword matching
- Prioritizes accessibility over perfect accuracy

The Python CLI version has **full system access**, which enables:
- Running ChromaDB vector database
- Loading and using embedding models
- Performing semantic similarity search
- More accurate retrieval at the cost of requiring local installation

## Future Enhancements

Potential improvements:
- Hybrid search (keywords + embeddings in web version)
- Multi-language support beyond German
- User feedback on citation relevance
- Improved keyword extraction algorithms
- Caching for backend API responses
