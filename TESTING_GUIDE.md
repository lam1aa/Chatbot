# Quick Testing Guide

This guide shows how to test the implemented features.

## Prerequisites

```bash
pip install -r requirements.txt
```

## Test 1: Verify URL Mapping Generation

```bash
python generate_url_mapping.py
```

**Expected Output:**
```
✓ Generated ./knowledge_base/url_mapping.json
  Mapped 27 TXT files to URLs

Examples:
  Antragsformulare.txt -> https://www.xn--bafg-7qa.de/...
  Fragen_und_Antworten.txt -> https://www.xn--bafg-7qa.de/...
  gibt-es-bafoeg-auch-im-ausland.txt -> https://www.xn--bafg-7qa.de/...
  ... and 24 more
```

## Test 2: Verify English UI

1. Open `index.html` in a web browser
2. Check that all text is in English:
   - ✓ "Your Assistant for BAföG Questions"
   - ✓ "API Key Required"
   - ✓ "Save" button
   - ✓ "Open Source on GitHub" (not "auf")

## Test 3: Test Backend API with Citations

### Step 1: Start Backend Server

```bash
python api_server.py
```

**Expected Output:**
```
Initializing knowledge base...
Loading documents from ./knowledge_base...
Loaded X documents
...
🚀 Starting BAföG Chatbot API server on port 5000
   Health check: http://localhost:5000/health
   Chat endpoint: http://localhost:5000/chat
   Debug mode: False
```

### Step 2: Test Health Endpoint

In another terminal:
```bash
curl http://localhost:5000/health
```

**Expected Output:**
```json
{
  "knowledge_base_loaded": true,
  "status": "ok"
}
```

### Step 3: Test Chat with Citations

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is BAföG?",
    "api_key": "your-openrouter-api-key-here"
  }'
```

**Expected Output:**
```json
{
  "answer": "BAföG is...",
  "sources": [
    {
      "name": "Bafoeg Info",
      "url": "https://www.bafög.de/...",
      "file": "bafoeg_info.txt"
    }
  ]
}
```

### Step 4: Test Web UI with Backend

1. Open `index.html` in browser
2. Open browser console (F12)
3. Look for: "Backend API available: true"
4. Enter your OpenRouter API key
5. Ask a question about BAföG
6. Response should include sources with clickable URLs!

## Test 4: Test Web UI Without Backend (Fallback)

1. Make sure backend is NOT running (stop api_server.py)
2. Refresh `index.html`
3. Open browser console
4. Look for: "Backend API not available, using direct OpenRouter calls"
5. Enter your OpenRouter API key
6. Ask a question
7. Response works but NO sources shown (as expected)

## Verification Checklist

- [x] ✅ URL mapping generated with 27 entries
- [x] ✅ All UI text is in English
- [x] ✅ Backend API server starts successfully
- [x] ✅ Health endpoint returns OK
- [x] ✅ Chat endpoint returns responses with sources
- [x] ✅ Web UI detects backend automatically
- [x] ✅ Web UI displays sources with clickable URLs
- [x] ✅ Web UI falls back gracefully when backend unavailable

## Troubleshooting

**Backend won't start:**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify .env file has OPENROUTER_API_KEY set

**No sources in responses:**
- Make sure backend API is running
- Check browser console for "Backend API available: true"
- Verify knowledge base files are in knowledge_base/ directory

**CORS errors:**
- Backend includes CORS support, should work from file:// and http://
- If issues persist, serve HTML via `python -m http.server 8080`

## Success Criteria

All three requirements are met when:
1. UI displays entirely in English ✅
2. url_mapping.json exists with 27 TXT file mappings ✅
3. Backend returns responses with source URLs ✅
4. Web UI shows citations when backend is running ✅
