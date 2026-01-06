// BAföG Chatbot Web Application
// This runs entirely in the browser and makes direct API calls to OpenRouter

class ChatbotApp {
    constructor() {
        this.apiKey = null;
        this.conversationHistory = [];
        this.isProcessing = false;
        this.knowledgeBase = [];
        this.urlMapping = {};
        
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
        // Load URL mapping
        await this.loadUrlMapping();
        
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
    
    async loadUrlMapping() {
        try {
            const response = await fetch('knowledge_base/url_mapping.json');
            if (response.ok) {
                this.urlMapping = await response.json();
                console.log('URL mapping loaded:', Object.keys(this.urlMapping).length, 'entries');
            }
        } catch (error) {
            console.error('Failed to load URL mapping:', error);
        }
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
            // Get response from OpenRouter API
            const response = await this.callOpenRouter(message);
            this.addMessage(response.answer, 'bot', response.sources);
        } catch (error) {
            console.error('Error:', error);
            this.addErrorMessage(error.message);
        } finally {
            this.setProcessing(false);
            this.userInput.focus();
        }
    }
    
    async callOpenRouter(userMessage) {
        // Build the conversation with context
        const systemPrompt = `You are a helpful assistant for BAföG questions. 
Answer questions about BAföG (Federal Training Assistance Act) in Germany.
Be precise, friendly, and helpful. If you don't know something, say so honestly.
Point out that amounts and regulations may change and current information should be obtained from the responsible BAföG office.

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
        
        // Extract potential source references from the response
        const sources = this.extractSources(assistantMessage);
        
        return {
            answer: assistantMessage,
            sources: sources
        };
    }
    
    extractSources(text) {
        // This is a simple heuristic - look for common document references
        // In a full RAG implementation, this would come from the retrieval step
        const sources = [];
        const lowerText = text.toLowerCase();
        
        // Check if any of our knowledge base files are referenced
        for (const [filename, url] of Object.entries(this.urlMapping)) {
            // Create searchable terms from filename
            const baseName = filename.replace('.txt', '').replace(/-/g, ' ');
            
            // If the response might reference this document, include it as a source
            // This is a simplified approach - a real RAG system would track actual sources
            if (lowerText.includes('student') || lowerText.includes('bafoeg') || 
                lowerText.includes('funding') || lowerText.includes('education')) {
                // For now, we'll include a few relevant sources
                // In production, this would be based on actual vector similarity search
            }
        }
        
        return sources;
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
