#!/usr/bin/env python3
"""
Knowledge Base Manager
Helper script to manage the knowledge base
"""
import os
import sys
import shutil
from scraper import WebScraper


def rebuild_vector_db():
    """Delete the vector database to force rebuild"""
    chroma_dir = "./chroma_db"
    if os.path.exists(chroma_dir):
        print(f"Deleting {chroma_dir}...")
        shutil.rmtree(chroma_dir)
        print("✓ Vector database deleted. It will be rebuilt on next run.")
    else:
        print("Vector database doesn't exist yet.")


def list_knowledge_files():
    """List all files in knowledge base"""
    kb_dir = "./knowledge_base"
    if not os.path.exists(kb_dir):
        print("Knowledge base directory doesn't exist!")
        return
    
    files = [f for f in os.listdir(kb_dir) if f.endswith('.txt')]
    
    if not files:
        print("No .txt files found in knowledge base.")
        return
    
    print(f"\nKnowledge base files ({len(files)}):")
    for f in sorted(files):
        filepath = os.path.join(kb_dir, f)
        size = os.path.getsize(filepath)
        print(f"  - {f} ({size} bytes)")


def scrape_from_urls():
    """Interactive scraping from URLs"""
    print("\n=== Web Scraping ===")
    print("Enter URLs to scrape (one per line).")
    print("Press Enter twice when done.\n")
    
    urls = []
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("No URLs provided.")
        return
    
    scraper = WebScraper()
    scraper.scrape_urls(urls)
    
    print("\n⚠️  Remember to rebuild the vector database:")
    print("    python kb_manager.py rebuild")


def main():
    if len(sys.argv) < 2:
        print("BAföG Knowledge Base Manager")
        print("\nUsage:")
        print("  python kb_manager.py list       - List all knowledge base files")
        print("  python kb_manager.py scrape     - Scrape content from URLs")
        print("  python kb_manager.py rebuild    - Rebuild vector database")
        print("\nExamples:")
        print("  python kb_manager.py list")
        print("  python kb_manager.py scrape")
        print("  python kb_manager.py rebuild")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_knowledge_files()
    elif command == "scrape":
        scrape_from_urls()
    elif command == "rebuild":
        rebuild_vector_db()
    else:
        print(f"Unknown command: {command}")
        print("Use: list, scrape, or rebuild")


if __name__ == "__main__":
    main()
