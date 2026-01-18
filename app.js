// BAföG Chatbot Web Application
// Client-side citations using keyword matching

class ChatbotApp {
    constructor() {
        this.apiKey = null;
        this.conversationHistory = [];
        this.isProcessing = false;
        this.knowledgeIndex = [];
        this.backendAvailable = false;
        this.backendUrl = 'http://localhost:5000';
        
        // UI Elements
        this.apiKeySection = document.getElementById('api-key-section');
        this.chatSection = document.getElementById('chat-section');
        this.apiKeyInput = document.getElementById('api-key-input');
        this.saveApiKeyBtn = document.getElementById('save-api-key');
        this.changeApiKeyBtn = document.getElementById('change-api-key');
        this.clearChatBtn = document.getElementById('clear-chat');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.messagesContainer = document.getElementById('messages');
        
        this.init();
    }
    
    async init() {
        // Load knowledge index for client-side citations
        await this.loadKnowledgeIndex();
        
        // Check if backend API is available (optional)
        await this.checkBackend();
        
        // Check if API key is stored
        this.loadApiKey();
        
        // Event listeners
        this.saveApiKeyBtn.addEventListener('click', () => this.saveApiKey());
        this.changeApiKeyBtn.addEventListener('click', () => this.changeApiKey());
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter to send (Shift+Enter for new line)
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = this.userInput.scrollHeight + 'px';
        });
        
        // Enter key in API key input
        this.apiKeyInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.saveApiKey();
            }
        });
    }
    
    async checkBackend() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 2000); // 2 second timeout
            
            const response = await fetch(`${this.backendUrl}/health`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const data = await response.json();
                this.backendAvailable = data.status === 'ok' && data.knowledge_base_loaded;
                console.log('Backend API available:', this.backendAvailable);
            }
        } catch (error) {
            this.backendAvailable = false;
            console.log('Backend API not available, using direct OpenRouter calls');
        }
    }
    
    async loadKnowledgeIndex() {
        try {
            const response = await fetch('knowledge_base/knowledge_index.json');
            if (response.ok) {
                this.knowledgeIndex = await response.json();
                console.log('Knowledge index loaded:', this.knowledgeIndex.length, 'documents');
            } else {
                console.warn('Knowledge index not found, citations will not be available');
            }
        } catch (error) {
            console.error('Failed to load knowledge index:', error);
        }
    }
    
    findRelevantSources(question) {
        /**
         * Find relevant sources based on keyword matching
         * This provides citations without needing a backend server
         */
        if (!this.knowledgeIndex || this.knowledgeIndex.length === 0) {
            return [];
        }
        
        // Extract keywords from question
        const questionLower = question.toLowerCase();
        
        // English to German term mappings for better matching
        const termMappings = {
            'study': 'studium',
            'studies': 'studium',
            'application': 'antrag',
            'apply': 'antrag',
            'money': 'förderung',
            'funding': 'förderung',
            'age': 'altersgrenze',
            'limit': 'grenze',
            'abroad': 'ausland',
            'foreign': 'ausland',
            'income': 'einkommen',
            'parents': 'eltern',
            'repayment': 'rückzahlung',
            'amount': 'höhe',
            'loan': 'darlehen',
            'grant': 'zuschuss',
            'bafoeg': 'bafög',
            'bafög': 'bafög'
        };
        
        const questionWords = questionLower
            .replace(/[^a-zäöüß\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 2);
        
        // Expand question words with German equivalents
        const expandedWords = new Set(questionWords);
        questionWords.forEach(word => {
            if (termMappings[word]) {
                expandedWords.add(termMappings[word]);
            }
        });
        
        // Score each document based on keyword matches
        const scoredDocs = this.knowledgeIndex.map(doc => {
            let score = 0;
            
            // Check each keyword in the document
            doc.keywords.forEach(keyword => {
                // Direct match with question words
                expandedWords.forEach(qword => {
                    if (keyword === qword) {
                        score += 10; // Exact match
                    } else if (keyword.includes(qword) && qword.length > 3) {
                        score += 5; // Partial match
                    } else if (qword.includes(keyword) && keyword.length > 3) {
                        score += 3; // Word contains keyword
                    }
                });
            });
            
            // Bonus for matching document name
            const docNameLower = doc.name.toLowerCase();
            expandedWords.forEach(qword => {
                if (docNameLower.includes(qword) && qword.length > 3) {
                    score += 15;
                }
            });
            
            return { ...doc, score };
        });
        
        // Sort by score and return top 3 relevant sources
        const relevantSources = scoredDocs
            .filter(doc => doc.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, 3)
            .map(doc => ({
                name: doc.name,
                url: doc.url,
                file: doc.file
            }));
        
        return relevantSources;
    }
    
    loadApiKey() {
        const stored = localStorage.getItem('openrouter_api_key');
        if (stored) {
            this.apiKey = stored;
            this.showChatInterface();
        } else {
            this.showApiKeyInterface();
        }
    }
    
    saveApiKey() {
        const key = this.apiKeyInput.value.trim();
        if (!key) {
            alert('Please enter an API key.');
            return;
        }
        
        if (!key.startsWith('sk-or-')) {
            alert('The API key should start with "sk-or-". Please check your key.');
            return;
        }
        
        this.apiKey = key;
        localStorage.setItem('openrouter_api_key', key);
        this.apiKeyInput.value = '';
        this.showChatInterface();
    }
    
    changeApiKey() {
        if (confirm('Do you really want to change the API key? The chat will be reset.')) {
            this.apiKey = null;
            localStorage.removeItem('openrouter_api_key');
            this.clearChat();
            this.showApiKeyInterface();
        }
    }
    
    showApiKeyInterface() {
        this.apiKeySection.style.display = 'block';
        this.chatSection.style.display = 'none';
    }
    
    showChatInterface() {
        this.apiKeySection.style.display = 'none';
        this.chatSection.style.display = 'flex';
        this.userInput.focus();
    }
    
    clearChat() {
        this.conversationHistory = [];
        this.messagesContainer.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    <strong>Welcome!</strong> I'm your BAföG assistant. 
                    Ask me your questions about BAföG and I'll be happy to help you.
                </div>
            </div>
        `;
    }
    
    isNonBafogResponse(answer) {
        /**
         * Detect if the response is a rejection message for non-BAföG questions
         * Returns true if the answer indicates the question is not BAföG-related
         */
        const lowerAnswer = answer.toLowerCase();
        
        // Check for common rejection phrases in both German and English
        const rejectionPhrases = [
            'can only help with bafög',
            'can only assist with bafög',
            'only answer questions related to bafög',
            'kann nur bei bafög',
            'kann nur fragen zu bafög',
            'ausschließlich für bafög',
            'nur bafög-fragen'
        ];
        
        return rejectionPhrases.some(phrase => lowerAnswer.includes(phrase));
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isProcessing) return;
        
        // Add user message to UI
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
        
        // Disable input while processing
        this.setProcessing(true);
        
        try {
            let response;
            // Try backend API first if available, otherwise use direct OpenRouter with client-side citations
            if (this.backendAvailable) {
                response = await this.callBackendAPI(message);
            } else {
                // Get response from OpenRouter
                response = await this.callOpenRouter(message);
                // Add client-side citations based on keyword matching
                let sources = this.findRelevantSources(message);
                
                // If no specific sources found, provide general BAföG information sources
                if (sources.length === 0 && this.knowledgeIndex.length > 0) {
                    sources = this.knowledgeIndex
                        .filter(doc => 
                            (doc.keywords && doc.keywords.includes('bafög')) ||
                            (doc.name && doc.name.toLowerCase().includes('bafoeg')) ||
                            (doc.name && doc.name.toLowerCase().includes('bafög'))
                        )
                        .slice(0, 2)
                        .map(doc => ({
                            name: doc.name,
                            url: doc.url,
                            file: doc.file
                        }));
                }
                
                response.sources = sources;
            }
            
            // Check if this is a non-BAföG question response (don't show sources)
            const isNonBafogResponse = this.isNonBafogResponse(response.answer);
            const sourcesToShow = isNonBafogResponse ? [] : response.sources;
            
            this.addMessage(response.answer, 'bot', sourcesToShow);
        } catch (error) {
            console.error('Error:', error);
            this.addErrorMessage(error.message);
        } finally {
            this.setProcessing(false);
            this.userInput.focus();
        }
    }
    
    async callBackendAPI(userMessage) {
        try {
            const response = await fetch(`${this.backendUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: userMessage,
                    api_key: this.apiKey
                })
            });
            
            if (!response.ok) {
                // If backend fails, fall back to direct OpenRouter
                console.log('Backend API failed, falling back to direct OpenRouter');
                this.backendAvailable = false;
                return await this.callOpenRouter(userMessage);
            }
            
            const data = await response.json();
            return {
                answer: data.answer,
                sources: data.sources || []
            };
        } catch (error) {
            // If backend is unreachable, fall back to direct OpenRouter
            console.log('Backend API unreachable, falling back to direct OpenRouter');
            this.backendAvailable = false;
            return await this.callOpenRouter(userMessage);
        }
    }
    
    async callOpenRouter(userMessage) {
        // Build the conversation with context
        const systemPrompt = `You are a helpful assistant for BAföG questions ONLY. 
Your sole purpose is to answer questions about BAföG (Federal Training Assistance Act) in Germany.

IMPORTANT RULE: You can ONLY answer questions related to BAföG. 
If the user asks about anything else (weather, sports, programming, other topics, etc.), politely respond with:
"I can only help with BAföG-related questions. Please ask me something about BAföG and I'll be happy to assist you."

For BAföG-related questions:
- Be precise, friendly, and helpful
- If you don't know something, say so honestly
- Point out that amounts and regulations may change and current information should be obtained from the responsible BAföG office

Important BAföG information:
- BAföG is a state funding for students and pupils in Germany
- The amount depends on parental income and your living situation
- There is a maximum rate for students (varies depending on living situation)
- The funding consists half of a grant and half of an interest-free loan
- Repayment begins several years after the end of the maximum funding period
- There is a repayment cap
- Application is made to the responsible student services or BAföG office

When providing information, if you have specific knowledge from documents, mention that you found this information in specific resources.`;

        const messages = [
            { role: 'system', content: systemPrompt },
            ...this.conversationHistory,
            { role: 'user', content: userMessage }
        ];
        
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
                'HTTP-Referer': window.location.href,
                'X-Title': 'BAföG Chatbot'
            },
            body: JSON.stringify({
                model: 'meta-llama/llama-3.1-8b-instruct',
                messages: messages,
                temperature: 0.7,
                max_tokens: 1000
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            if (response.status === 401) {
                throw new Error('Invalid API key. Please check your OpenRouter API key.');
            } else if (response.status === 429) {
                throw new Error('Too many requests. Please wait a moment and try again.');
            } else if (response.status === 400 && errorData.error?.message?.includes('No endpoints found')) {
                throw new Error('The selected model is not available. Please try another model or check available models at openrouter.ai/models');
            } else {
                throw new Error(errorData.error?.message || `API error: ${response.status}`);
            }
        }
        
        const data = await response.json();
        const assistantMessage = data.choices[0]?.message?.content;
        
        if (!assistantMessage) {
            throw new Error('No response received from server.');
        }
        
        // Update conversation history (keep last 10 messages to avoid token limits)
        this.conversationHistory.push(
            { role: 'user', content: userMessage },
            { role: 'assistant', content: assistantMessage }
        );
        
        // Keep only last 10 messages (5 exchanges)
        if (this.conversationHistory.length > 10) {
            this.conversationHistory = this.conversationHistory.slice(-10);
        }
        
        // Return answer (sources will be added by sendMessage using client-side matching)
        return {
            answer: assistantMessage,
            sources: [] // Will be populated by findRelevantSources in sendMessage
        };
    }
    
    addMessage(text, type, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        
        // Add sources if available (for bot messages)
        if (type === 'bot' && sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources';
            sourcesDiv.innerHTML = '<strong>📚 Sources:</strong><br>';
            
            sources.forEach(source => {
                const sourceLink = document.createElement('a');
                sourceLink.href = source.url;
                sourceLink.target = '_blank';
                sourceLink.textContent = source.name;
                sourceLink.style.display = 'block';
                sourceLink.style.marginTop = '4px';
                sourcesDiv.appendChild(sourceLink);
            });
            
            messageDiv.appendChild(sourcesDiv);
        }
        
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    addErrorMessage(errorText) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message error-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<strong>⚠️ Error:</strong> ${errorText}`;
        
        messageDiv.appendChild(contentDiv);
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    setProcessing(isProcessing) {
        this.isProcessing = isProcessing;
        this.sendButton.disabled = isProcessing;
        this.userInput.disabled = isProcessing;
        
        const sendIcon = document.getElementById('send-icon');
        const loadingSpinner = document.getElementById('loading-spinner');
        
        if (isProcessing) {
            sendIcon.style.display = 'none';
            loadingSpinner.style.display = 'inline-block';
        } else {
            sendIcon.style.display = 'inline-block';
            loadingSpinner.style.display = 'none';
        }
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotApp();
});
