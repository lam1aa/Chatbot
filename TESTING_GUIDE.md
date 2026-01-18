# Testing Guide

Quick guide to test the BAföG Chatbot implementation.

## Prerequisites

For Python CLI testing:
```bash
pip install -r requirements.txt
```

## Test 1: Web Version (Recommended)

### Test in Browser

1. Open `index.html` in a web browser
2. Verify the interface is in English:
   - ✓ "Your Assistant for BAföG Questions"
   - ✓ "API Key Required"
   - ✓ "Save" button
   - ✓ "Open Source on GitHub"

3. Enter an OpenRouter API key
4. Ask a question (e.g., "What is BAföG?")
5. Verify response appears with citations
6. Check that source URLs are clickable

### Test Citations

1. Ask: "How do I apply for BAföG?"
2. Expected: Response with citations showing relevant documents
3. Click a source URL to verify it opens the correct page

### Test Online Version

Visit: https://lam1aa.github.io/Chatbot/

Verify same functionality works on deployed version.

## Test 2: Python CLI Version

### Test Basic Setup

```bash
# Run the chatbot
python main.py
```

Expected output:
```
Loading documents from ./knowledge_base...
Loaded X documents
Creating embeddings...
[Chat interface starts]
```

### Test Knowledge Base Management

```bash
# List files
python kb_manager.py list
```

Expected: List of all .txt files in knowledge_base/

```bash
# Rebuild vector database
python kb_manager.py rebuild
```

Expected: Success message about rebuilding ChromaDB

## Test 3: URL Mapping

### Verify URL Mapping Exists

```bash
ls -l knowledge_base/url_mapping.json
```

Expected: File exists with recent timestamp

### Check Mapping Content

```bash
python -c "import json; data=json.load(open('knowledge_base/url_mapping.json')); print(f'{len(data)} files mapped'); print(list(data.items())[:3])"
```

Expected: Shows number of mapped files and sample entries

## Test 4: Optional Backend API

### Start Backend

```bash
python api_server.py
```

Expected output:
```
Initializing knowledge base...
Knowledge base loaded successfully!
🚀 Starting BAföG Chatbot API server on port 5000
```

### Test Health Endpoint

In another terminal:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "knowledge_base_loaded": true,
  "status": "ok"
}
```

### Test Chat Endpoint

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Was ist BAföG?", "api_key": "YOUR_API_KEY"}'
```

Expected: JSON response with answer and sources

### Test Web UI with Backend

1. Keep backend running
2. Open index.html
3. Open browser console (F12)
4. Look for: "Backend API available: true"
5. Ask a question
6. Verify citations appear from backend

## Test 5: Web Scraper

### Test Scraping (Optional)

```bash
python kb_manager.py scrape
```

Enter a test URL when prompted, e.g.:
```
https://www.bafög.de/bafoeg/de/home/home_node.html
```

Expected:
- File saved in knowledge_base/
- URL added to url_mapping.json

## Verification Checklist

After running tests, verify:

- [ ] ✅ Web UI displays in English
- [ ] ✅ Web UI shows citations with URLs
- [ ] ✅ Python CLI starts without errors
- [ ] ✅ Knowledge base loads successfully
- [ ] ✅ url_mapping.json exists with entries
- [ ] ✅ Backend API (if tested) starts and responds
- [ ] ✅ Health endpoint returns OK
- [ ] ✅ Chat endpoint returns responses with sources
- [ ] ✅ Web UI detects backend when available

## Troubleshooting

**Web UI not showing citations:**
- Check browser console for errors
- Verify knowledge_base/knowledge_index.json exists
- Try hard refresh (Ctrl+Shift+R)

**Python CLI errors:**
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check .env file has OPENROUTER_API_KEY set
- Ensure knowledge_base/ directory has .txt files

**Backend won't start:**
- Check port 5000 is not in use
- Verify Flask is installed: `pip install flask flask-cors`
- Check knowledge_base files exist

**CORS errors with backend:**
- Backend includes CORS support
- If issues persist, serve HTML via: `python -m http.server 8080`

## Success Criteria

All tests pass when:
1. ✅ Web version works standalone with citations
2. ✅ Python CLI can answer questions with sources
3. ✅ URL mapping contains file-to-URL mappings
4. ✅ Backend API (optional) provides enhanced RAG responses
5. ✅ All documentation matches actual behavior
