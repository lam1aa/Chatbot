# BAföG RAG Chatbot

A minimal RAG (Retrieval-Augmented Generation) chatbot for answering BAföG-related questions using open-source technologies.

## 🌐 Try it Online

**[Try the Web Version](https://lam1aa.github.io/Chatbot/)** - No installation required!

The chatbot is available as both a web application (browser-based) and a command-line tool (Python).

## Features

- 🤖 Uses OpenRouter API for LLM (free models available)
- 🌐 **Web interface** - Share via GitHub Pages link
- 📚 ChromaDB for vector storage (open-source, for Python version)
- 🔍 Semantic search over BAföG documentation (Python version)
- 🌐 Built-in web scraper for BAföG websites
- 📎 Source attribution with URLs in responses
- 🔄 Automatic knowledge base updates
- 🚀 Simple and minimal codebase
- 🇩🇪 German language support
- 📱 Responsive design (mobile & desktop)

## Architecture

### Web Version
- **Frontend**: HTML, CSS, JavaScript (static files)
- **LLM**: Direct API calls to OpenRouter from browser
- **Deployment**: GitHub Pages (free hosting)

### Python Version
- **LLM**: OpenRouter API (supports various open-source models)
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB (open-source, local storage)
- **Framework**: LangChain

## Quick Start

### 🌐 Web Version (Recommended for Sharing)

The easiest way to use and share the chatbot:

1. Visit **[https://lam1aa.github.io/Chatbot/](https://lam1aa.github.io/Chatbot/)**
2. Get a free API key from [OpenRouter.ai](https://openrouter.ai/)
3. Enter your API key in the web interface
4. Start chatting!

**For RAG with source citations**: Run the backend API server (see below) alongside the web interface.

**Want to deploy your own?** See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for detailed instructions.

### 🔌 Web + Backend API (RAG with Citations)

For the full experience with source citations from the knowledge base:

1. Start the backend API server:

```bash
python api_server.py
```

2. Open `index.html` in your browser or visit the deployed web version
3. The web interface will automatically detect and use the backend API
4. You'll get responses with source citations and URLs!

The backend provides:
- ✅ RAG-based responses from knowledge base
- ✅ Source citations with URLs
- ✅ Semantic search over documents
- ✅ Fallback to direct OpenRouter if backend unavailable

### 🖥️ Python CLI Version (Advanced)

For local development with RAG capabilities and custom knowledge base:

#### Automated Setup (Recommended)

```bash
bash setup.sh
```

Then edit `.env` to add your OpenRouter API key and run:

```bash
python main.py
```

#### Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Add Knowledge Base

Place your scraped BAföG `.txt` files in the `knowledge_base/` directory. Two sample files are already included.

#### 3. Configure API Key

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_api_key_here
```

**Get a free API key at**: https://openrouter.ai/

#### 4. Run the Chatbot

```bash
python main.py
```

## Usage

### Interactive Mode

Once running, you can ask questions in German:

```
Du: Was ist BAföG?
Bot: [Answer based on your knowledge base]

Quellen:
📄 knowledge_base/bafoeg_info.txt
   🔗 https://www.bafög.de/bafoeg/de/home/home_node.html

Du: Wie hoch ist die Förderung?
Bot: [Answer based on your knowledge base]

Quellen:
📄 knowledge_base/bafoeg_info.txt
   🔗 https://www.bafög.de/bafoeg/de/home/home_node.html

Du: exit
```

### Programmatic Usage

You can also use the chatbot in your own Python scripts:

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

# Access sources
for source in result["sources"]:
    print(f"Source: {source.metadata['source']}")
    if 'url' in source.metadata:
        print(f"URL: {source.metadata['url']}")
```

See `example_usage.py` for a complete example.

## Managing Knowledge Base

### Option 1: Use Pre-scraped Files with URL Mapping

1. Add your `.txt` files to `knowledge_base/` directory
2. Create/update `knowledge_base/url_mapping.json` to map files to source URLs:

```json
{
  "bafoeg_info.txt": "https://www.bafög.de/bafoeg/de/home/home_node.html",
  "antragstellung.txt": "https://www.bafög.de/bafoeg/de/antrag-stellen/antrag-stellen_node.html"
}
```

3. Rebuild the vector database:

```bash
python kb_manager.py rebuild
```

### Option 2: Scrape Directly from URLs

Use the built-in web scraper to fetch content from BAföG websites:

```bash
# Interactive mode
python kb_manager.py scrape
```

Or edit `scraper.py` and add your URLs, then run:

```bash
python scraper.py
```

**See [SCRAPING_GUIDE.md](SCRAPING_GUIDE.md) for detailed scraping instructions and example URLs.**

### Knowledge Base Commands

```bash
# List all knowledge base files
python kb_manager.py list

# Scrape content from URLs
python kb_manager.py scrape

# Rebuild vector database (after adding new files)
python kb_manager.py rebuild
```

**Note:** After adding new files or scraping, always rebuild the vector database to include the new content.

## Project Structure

```
.
├── # Web Interface Files (for GitHub Pages)
├── index.html                   # Main web interface
├── styles.css                   # Web UI styling
├── app.js                       # Web application logic (supports backend API)
├── api_server.py               # Backend API server for RAG with citations
├── WEB_DEPLOYMENT.md           # Web deployment guide
│
├── # Python CLI Files
├── knowledge_base/              # Place your BAföG .txt files here
│   ├── bafoeg_info.txt         # Sample: General BAföG information
│   ├── antragstellung.txt      # Sample: Application process info
│   ├── URLs.csv                # CSV file mapping filenames to URLs
│   └── url_mapping.json        # Generated JSON mapping of files to URLs
├── src/
│   ├── knowledge_base_loader.py  # Loads and processes documents
│   └── rag_chatbot.py           # RAG chatbot implementation
├── main.py                      # Entry point - interactive chat
├── example_usage.py            # Example of programmatic usage
├── scraper.py                  # Web scraper for BAföG websites
├── kb_manager.py               # Knowledge base management tool
├── generate_url_mapping.py     # Generate url_mapping.json from URLs.csv
├── setup.sh                    # Automated setup script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Configuration

### LLM Model

You can change the model in `.env`:

```
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

See available models at: https://openrouter.ai/models

**Note:** If you encounter "No endpoints found" errors, try removing the `:free` suffix from the model name or select a different model from the OpenRouter models page.

### Retrieval Settings

Edit `src/rag_chatbot.py` to adjust:
- `search_kwargs={"k": 3}` - Number of documents to retrieve
- `temperature=0.7` - LLM creativity (0.0-1.0)

## Adding More Documents

1. Place `.txt` files in `knowledge_base/` directory
2. Delete `chroma_db/` directory (if exists)
3. Run `python main.py` to rebuild the vector database

## 🚀 Deployment

### GitHub Pages (Web Version)

Deploy the web interface to GitHub Pages for free hosting:

1. Push your changes to GitHub
2. Go to **Settings** → **Pages**
3. Select **Branch: main** and **Folder: / (root)**
4. Click **Save**
5. Your chatbot will be available at `https://<username>.github.io/Chatbot/`

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for detailed deployment instructions.

### Differences Between Versions

| Feature | Web Version (No Backend) | Web + Backend API | Python CLI Version |
|---------|-------------|-------------------|-------------------|
| **Accessibility** | Browser-based, shareable link | Browser + local server | Local installation required |
| **Knowledge Base** | General BAföG knowledge | Custom documents via ChromaDB | Custom documents via ChromaDB |
| **RAG Search** | ❌ (Direct LLM) | ✅ (Vector search) | ✅ (Vector search) |
| **Source Citations** | ❌ | ✅ With URLs | ✅ With URLs |
| **Setup** | Just API key | API key + Python server | Python environment + dependencies |
| **Sharing** | Easy (just share link) | Requires backend server | Requires users to install |
| **Customization** | Edit prompt in app.js | Full control over RAG pipeline | Full control over RAG pipeline |

## Notes

- **Web Version**: Uses direct API calls from browser to OpenRouter. No server required.
- **Python Version**: The vector database is created on first run and persisted in `chroma_db/`
- All components are open-source except the OpenRouter API (which provides free tier)
- Documents are split into 1000-character chunks with 100-character overlap for better context (Python version)

## License

MIT