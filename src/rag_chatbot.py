"""
RAG Chatbot
Retrieval-Augmented Generation chatbot for BAföG questions
"""
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.callbacks import get_openai_callback


class RAGChatbot:
    def __init__(self, vectorstore, api_key=None, model=None):
        load_dotenv()
        
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b")
        # self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
        # self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
        # self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in .env file")
        
        # Initialize LLM with OpenRouter
        # Note: Using OpenAI-compatible API with OpenRouter's endpoint
        self.llm = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            model=self.model,
            temperature=0.7,
        )
        
        # Create retriever from vector store
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Create custom prompt template
        template = """Du bist ein hilfreicher Assistent AUSSCHLIESSLICH für BAföG-Fragen. 

WICHTIGE REGEL: Du kannst NUR Fragen zu BAföG beantworten.
Falls der Benutzer nach etwas anderem fragt (Wetter, Sport, Programmierung, andere Themen usw.), antworte höflich:
"Ich kann nur bei BAföG-bezogenen Fragen helfen. Bitte stellen Sie mir eine Frage zu BAföG und ich helfe Ihnen gerne weiter."

Für BAföG-bezogene Fragen:
- Benutze einfache und leicht verständliche Sprache
- Erkläre komplizierte Begriffe in einfachen Worten
- Vermeide Fachsprache und schwierige Ausdrücke
- Benutze kurze, klare Sätze
- Benutze die folgenden Kontextinformationen, um die Frage zu beantworten
- Wenn du die Antwort nicht weißt, sage einfach, dass du es nicht weißt. Erfinde keine Antwort.

Kontext:
{context}

Frage: {question}

Hilfreiche Antwort:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def ask(self, question):
        """Ask a question and get an answer with token usage tracking"""
        try:
            # Note: get_openai_callback() is designed for OpenAI API and may not work
            # correctly with OpenRouter's custom base_url. Token usage from the callback
            # might be zero or incorrect. However, we still try to use it for compatibility.
            with get_openai_callback() as cb:
                result = self.qa_chain.invoke({"query": question})
                
                # Extract token usage information from callback
                token_usage = {
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_tokens": cb.total_tokens
                } if cb.total_tokens > 0 else None
                
                return {
                    "answer": result["result"],
                    "sources": result["source_documents"],
                    "token_usage": token_usage
                }
        except Exception as e:
            # If callback fails, return without token usage
            print(f"Token usage tracking failed: {e}")
            result = self.qa_chain.invoke({"query": question})
            return {
                "answer": result["result"],
                "sources": result["source_documents"],
                "token_usage": None
            }
    
    def format_sources(self, sources):
        """Format source documents for display"""
        if not sources:
            return "Keine Quellen gefunden."
        
        formatted = []
        seen_sources = set()
        
        for doc in sources:
            source = doc.metadata.get('source', 'Unbekannt')
            # Get URL if available in metadata
            url = doc.metadata.get('url', '')
            
            # Create unique identifier
            source_id = f"{source}|{url}"
            if source_id in seen_sources:
                continue
            seen_sources.add(source_id)
            
            # Format source display
            if url:
                formatted.append(f"📄 {source}\n   🔗 {url}")
            else:
                formatted.append(f"📄 {source}")
        
        return "\n".join(formatted)
    
    def chat(self):
        """Interactive chat loop"""
        print("\n=== BAföG Chatbot ===")
        print("Stelle deine Fragen zu BAföG. Tippe 'exit' zum Beenden.\n")
        
        while True:
            question = input("Du: ").strip()
            
            if question.lower() in ['exit', 'quit', 'bye']:
                print("Auf Wiedersehen!")
                break
            
            if not question:
                continue
            
            try:
                result = self.ask(question)
                print(f"\nBot: {result['answer']}\n")
                
                # Only display sources if this is a BAföG-related question
                if not self._is_non_bafog_response(result['answer']):
                    sources_text = self.format_sources(result['sources'])
                    print(f"Quellen:\n{sources_text}\n")
                
            except Exception as e:
                print(f"Fehler: {str(e)}\n")
    
    def _is_non_bafog_response(self, answer):
        """
        Detect if the response is a rejection message for non-BAföG questions
        Returns True if the answer indicates the question is not BAföG-related
        
        Note: These phrases match the rejection message in the prompt template (line 42).
        A similar check exists in app.js for the web interface.
        """
        answer_lower = answer.lower()
        
        # Check for the rejection phrases in German
        # These correspond to the rejection message in the prompt template
        rejection_phrases = [
            'kann nur bei bafög',
            'kann nur fragen zu bafög',
            'ausschließlich für bafög',
            'nur bafög-fragen'
        ]
        
        return any(phrase in answer_lower for phrase in rejection_phrases)
