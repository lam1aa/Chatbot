# BAföG RAG Chatbot

A minimal RAG (Retrieval-Augmented Generation) chatbot for answering BAföG-related questions using open-source technologies.

## Features

- 🤖 Uses OpenRouter API for LLM (free models available)
- 📚 ChromaDB for vector storage (open-source)
- 🔍 Semantic search over BAföG documentation
- 🚀 Simple and minimal codebase
- 🇩🇪 German language support

## Architecture

- **LLM**: OpenRouter API (supports various open-source models)
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB (open-source, local storage)
- **Framework**: LangChain

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Knowledge Base

Place your scraped BAföG `.txt` files in the `knowledge_base/` directory. A sample file is already included.

### 3. Configure API Key

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_api_key_here
```

**Get a free API key at**: https://openrouter.ai/

### 4. Run the Chatbot

```bash
python main.py
```

## Usage

Once running, you can ask questions in German:

```
Du: Was ist BAföG?
Bot: [Answer based on your knowledge base]

Du: Wie hoch ist die Förderung?
Bot: [Answer based on your knowledge base]

Du: exit
```

## Project Structure

```
.
├── knowledge_base/          # Place your BAföG .txt files here
│   └── bafoeg_info.txt     # Sample knowledge base
├── src/
│   ├── knowledge_base_loader.py  # Loads and processes documents
│   └── rag_chatbot.py           # RAG chatbot implementation
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
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