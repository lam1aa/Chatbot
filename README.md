# BAföG RAG Chatbot

A minimal RAG (Retrieval-Augmented Generation) chatbot for answering BAföG-related questions.

## 🌐 Try it Online

**[Try the Web Version](https://lam1aa.github.io/Chatbot/)** - No installation required!

- ✅ Works entirely in your browser
- ✅ Automatic source citations with clickable URLs
- ✅ Just needs an OpenRouter API key (free tier available)
- ✅ No backend server needed

See [citation_demo.html](citation_demo.html) for citation examples.

## Features

**Web Version (Recommended for most users):**
- 🌐 Browser-based - works on any device
- 📎 Client-side source citations with URLs
- 🔑 Just needs an OpenRouter API key
- 📱 Responsive design (mobile & desktop)
- 🇩🇪 German language support

**Python CLI Version (For advanced users):**
- 📚 ChromaDB for vector storage
- 🔍 Semantic search over custom documents
- 🌐 Built-in web scraper for BAföG websites
- 🔄 Knowledge base management tools

## Quick Start

### 🌐 Web Version (Easiest)

1. Visit **[https://lam1aa.github.io/Chatbot/](https://lam1aa.github.io/Chatbot/)**
2. Get a free API key from [OpenRouter.ai](https://openrouter.ai/)
3. Enter your API key
4. Start chatting - citations included automatically!

Want to deploy your own? See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md).

### 🖥️ Python CLI Version

For local development with custom knowledge base:

```bash
# Automated setup
bash setup.sh

# Edit .env to add your OpenRouter API key, then:
python main.py
```

See sections below for manual setup and advanced options.

## Python CLI Setup (Advanced)

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Add Knowledge Base

Place your BAföG `.txt` files in the `knowledge_base/` directory. Sample files are included.

#### 3. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key from https://openrouter.ai/

#### 4. Run the Chatbot

```bash
python main.py
```

## Usage Examples

### Web Interface

Just visit the web version and ask questions like:
- "Was ist BAföG?"
- "Wie stelle ich einen Antrag?"
- "Gibt es eine Altersgrenze?"

Citations appear automatically with clickable source URLs.

### Python CLI

```python
from src.knowledge_base_loader import KnowledgeBaseLoader
from src.rag_chatbot import RAGChatbot

# Load knowledge base
kb_loader = KnowledgeBaseLoader()
vectorstore = kb_loader.setup()

# Initialize chatbot
chatbot = RAGChatbot(vectorstore)

# Ask questions
result = chatbot.ask("Was ist BAföG?")
print(result["answer"])
```

See `example_usage.py` for more details.

## Managing Knowledge Base (Python CLI)

### Add New Documents

1. Add `.txt` files to `knowledge_base/` directory
2. Update `knowledge_base/url_mapping.json` (optional, for source URLs):
   ```json
   {
     "your_file.txt": "https://source-url.de"
   }
   ```
3. Rebuild vector database:
   ```bash
   python kb_manager.py rebuild
   ```

### Scrape Content from Web

```bash
# Interactive mode
python kb_manager.py scrape

# List files
python kb_manager.py list
```

See [SCRAPING_GUIDE.md](SCRAPING_GUIDE.md) for details.

## Project Structure

```
├── # Web Interface (GitHub Pages)
├── index.html              # Main web UI
├── styles.css              # Styling
├── app.js                  # Web app logic + client-side citations
├── citation_demo.html      # Citation examples
├── knowledge_base/
│   ├── *.txt              # BAföG documents
│   ├── knowledge_index.json  # Index for web citations
│   └── url_mapping.json   # File-to-URL mapping
│
├── # Python CLI
├── src/
│   ├── knowledge_base_loader.py
│   └── rag_chatbot.py
├── main.py                # CLI entry point
├── kb_manager.py          # Knowledge base tools
├── api_server.py          # Optional backend API
└── requirements.txt
```

## Configuration

### Web Version
Edit `app.js` to customize:
- LLM model (line ~270): `model: 'meta-llama/llama-3.1-8b-instruct'`
- System prompt for chatbot behavior

### Python CLI
Edit `.env` for LLM model:
```
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

See available models at: https://openrouter.ai/models

## Deployment

### GitHub Pages (Recommended)

The web version can be deployed for free:

1. Push to GitHub
2. Go to **Settings** → **Pages**
3. Select **Branch: main** and **Folder: / (root)**
4. Save - your chatbot will be at `https://<username>.github.io/Chatbot/`

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for details.

## Architecture

### Web Version
- **Frontend**: Static HTML/CSS/JavaScript
- **Citations**: Client-side keyword matching with knowledge_index.json
- **LLM**: Direct OpenRouter API calls from browser
- **Hosting**: GitHub Pages or any static host

### Python CLI Version
- **LLM**: OpenRouter API
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (local)
- **Framework**: LangChain

### Optional Backend API
For advanced RAG with semantic search:
```bash
python api_server.py
```
Provides vector-based retrieval instead of keyword matching.

## How It Works

**Web Version:**
1. Loads knowledge_index.json on page load (26+ documents)
2. User asks a question
3. Keywords extracted and matched against document index
4. LLM generates response via OpenRouter
5. Relevant sources displayed with URLs

**Python CLI:**
1. Documents split into chunks and embedded
2. User question embedded
3. Similar chunks retrieved from ChromaDB
4. LLM generates answer using retrieved context
5. Sources displayed with URLs

## License

MIT