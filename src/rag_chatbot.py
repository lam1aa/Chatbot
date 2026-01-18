"""
RAG Chatbot
Retrieval-Augmented Generation chatbot for BAföG questions
"""
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI


class RAGChatbot:
    def __init__(self, vectorstore, api_key=None, model=None):
        load_dotenv()
        
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
        
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
        """Ask a question and get an answer"""
        result = self.qa_chain.invoke({"query": question})
        return {
            "answer": result["result"],
            "sources": result["source_documents"]
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
        """
        answer_lower = answer.lower()
        
        # Check for the rejection phrase in German
        rejection_phrases = [
            'kann nur bei bafög',
            'kann nur fragen zu bafög',
            'ausschließlich für bafög',
            'nur bafög-fragen'
        ]
        
        return any(phrase in answer_lower for phrase in rejection_phrases)
