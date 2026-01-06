# BAföG RAG Chatbot

A minimal RAG (Retrieval-Augmented Generation) chatbot for answering BAföG-related questions using open-source technologies.

## Features

- 🤖 Uses OpenRouter API for LLM (free models available)
- 📚 ChromaDB for vector storage (open-source)
- 🔍 Semantic search over BAföG documentation
- 🌐 Built-in web scraper for BAföG websites
- 📎 Source attribution with URLs in responses
- 🔄 Automatic knowledge base updates
- 🚀 Simple and minimal codebase
- 🇩🇪 German language support

## Architecture

- **LLM**: OpenRouter API (supports various open-source models)
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB (open-source, local storage)
- **Framework**: LangChain

## Quick Start

### Automated Setup (Recommended)

```bash
bash setup.sh
```

Then edit `.env` to add your OpenRouter API key and run:

```bash
python main.py
```

### Manual Setup

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
├── knowledge_base/              # Place your BAföG .txt files here
│   ├── bafoeg_info.txt         # Sample: General BAföG information
│   ├── antragstellung.txt      # Sample: Application process info
│   └── url_mapping.json        # Maps filenames to source URLs
├── src/
│   ├── knowledge_base_loader.py  # Loads and processes documents
│   └── rag_chatbot.py           # RAG chatbot implementation
├── main.py                      # Entry point - interactive chat
├── example_usage.py            # Example of programmatic usage
├── scraper.py                  # Web scraper for BAföG websites
├── kb_manager.py               # Knowledge base management tool
├── setup.sh                    # Automated setup script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Configuration

### LLM Model

You can change the model in `.env`:

```
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

See available models at: https://openrouter.ai/models

### Retrieval Settings

Edit `src/rag_chatbot.py` to adjust:
- `search_kwargs={"k": 3}` - Number of documents to retrieve
- `temperature=0.7` - LLM creativity (0.0-1.0)

## Adding More Documents

1. Place `.txt` files in `knowledge_base/` directory
2. Delete `chroma_db/` directory (if exists)
3. Run `python main.py` to rebuild the vector database

## Notes

- The vector database is created on first run and persisted in `chroma_db/`
- All components are open-source except the OpenRouter API (which provides free tier)
- Documents are split into 500-character chunks with 50-character overlap

## License

MIT