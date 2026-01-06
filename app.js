// BAföG Chatbot Web Application
// This runs entirely in the browser and makes direct API calls to OpenRouter

class ChatbotApp {
    constructor() {
        this.apiKey = null;
        this.conversationHistory = [];
        this.isProcessing = false;
        
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
    
    init() {
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
            alert('Bitte gib einen API-Schlüssel ein.');
            return;
        }
        
        if (!key.startsWith('sk-or-')) {
            alert('Der API-Schlüssel sollte mit "sk-or-" beginnen. Bitte überprüfe deinen Schlüssel.');
            return;
        }
        
        this.apiKey = key;
        localStorage.setItem('openrouter_api_key', key);
        this.apiKeyInput.value = '';
        this.showChatInterface();
    }
    
    changeApiKey() {
        if (confirm('Möchtest du wirklich den API-Schlüssel ändern? Der Chat wird zurückgesetzt.')) {
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
                    <strong>Willkommen!</strong> Ich bin dein BAföG-Assistent. 
                    Stelle mir deine Fragen zu BAföG und ich helfe dir gerne weiter.
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
            this.addMessage(response, 'bot');
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
        const systemPrompt = `Du bist ein hilfreicher Assistent für BAföG-Fragen. 
Beantworte Fragen zu BAföG (Bundesausbildungsförderungsgesetz) in Deutschland auf Deutsch.
Sei präzise, freundlich und hilfreich. Wenn du etwas nicht weißt, sage es ehrlich.
Weise darauf hin, dass Beträge und Regelungen sich ändern können und aktuelle Informationen beim zuständigen BAföG-Amt eingeholt werden sollten.

Wichtige BAföG-Informationen:
- BAföG ist eine staatliche Förderung für Studierende und Schüler in Deutschland
- Die Höhe hängt vom Einkommen der Eltern und der eigenen Wohnsituation ab
- Es gibt einen Höchstsatz für Studierende (variiert je nach Wohnsituation)
- Die Förderung besteht zur Hälfte aus einem Zuschuss und zur Hälfte aus einem zinslosen Darlehen
- Die Rückzahlung beginnt einige Jahre nach Ende der Förderungshöchstdauer
- Es gibt eine Rückzahlungsobergrenze
- Antragstellung erfolgt beim zuständigen Studierendenwerk oder BAföG-Amt`;

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
                throw new Error('Ungültiger API-Schlüssel. Bitte überprüfe deinen OpenRouter API-Schlüssel.');
            } else if (response.status === 429) {
                throw new Error('Zu viele Anfragen. Bitte warte einen Moment und versuche es erneut.');
            } else if (response.status === 400 && errorData.error?.message?.includes('No endpoints found')) {
                throw new Error('Das ausgewählte Modell ist nicht verfügbar. Bitte versuche ein anderes Modell oder überprüfe die verfügbaren Modelle auf openrouter.ai/models');
            } else {
                throw new Error(errorData.error?.message || `API-Fehler: ${response.status}`);
            }
        }
        
        const data = await response.json();
        const assistantMessage = data.choices[0]?.message?.content;
        
        if (!assistantMessage) {
            throw new Error('Keine Antwort vom Server erhalten.');
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
        
        return assistantMessage;
    }
    
    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    addErrorMessage(errorText) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message error-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<strong>⚠️ Fehler:</strong> ${errorText}`;
        
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
