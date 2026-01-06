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
        self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in .env file")
        
        # Initialize LLM with OpenRouter
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
        template = """Du bist ein hilfreicher Assistent für BAföG-Fragen. 
Benutze die folgenden Kontextinformationen, um die Frage zu beantworten.
Wenn du die Antwort nicht weißt, sage einfach, dass du es nicht weißt. Erfinde keine Antwort.

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
            except Exception as e:
                print(f"Fehler: {str(e)}\n")
