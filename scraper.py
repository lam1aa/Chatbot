"""
Web Scraper for BAföG Information
Scrapes content from provided URLs and saves to knowledge base
"""
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time


class WebScraper:
    def __init__(self, output_dir="./knowledge_base"):
        self.output_dir = output_dir
        self.url_mapping = {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def scrape_url(self, url, delay=1):
        """Scrape content from a single URL"""
        print(f"Scraping: {url}")
        
        try:
            # Add delay to be respectful to the server
            time.sleep(delay)
            
            # Send request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            
            return text
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def generate_filename(self, url):
        """Generate a filename from URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('/', '_')
        if not path:
            path = parsed.netloc.replace('.', '_')
        
        # Ensure it ends with .txt
        if not path.endswith('.txt'):
            path += '.txt'
        
        return path
    
    def scrape_urls(self, urls):
        """Scrape multiple URLs and save to knowledge base"""
        print(f"\nScraping {len(urls)} URLs...\n")
        
        for url in urls:
            # Scrape content
            content = self.scrape_url(url)
            
            if content:
                # Generate filename
                filename = self.generate_filename(url)
                filepath = os.path.join(self.output_dir, filename)
                
                # Save content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Source: {url}\n\n")
                    f.write(content)
                
                # Update mapping
                self.url_mapping[filename] = url
                
                print(f"✓ Saved to: {filename}\n")
            else:
                print(f"✗ Failed to scrape: {url}\n")
        
        # Save URL mapping
        self._save_url_mapping()
        
        print(f"Scraping complete! Scraped {len(self.url_mapping)} pages.")
    
    def _save_url_mapping(self):
        """Save URL mapping to JSON file"""
        mapping_file = os.path.join(self.output_dir, "url_mapping.json")
        
        # Load existing mapping if it exists
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                existing_mapping = json.load(f)
            # Merge with new mapping
            existing_mapping.update(self.url_mapping)
            self.url_mapping = existing_mapping
        
        # Save updated mapping
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.url_mapping, f, ensure_ascii=False, indent=2)
        
        print(f"✓ URL mapping saved to: {mapping_file}")


def main():
    """Example usage"""
    scraper = WebScraper()
    
    # Example URLs - replace with your actual BAföG URLs
    urls = [
        "https://www.bafög.de/bafoeg/de/home/home_node.html",
        "https://www.bafög.de/bafoeg/de/das-bafoeg/das-bafoeg_node.html",
        "https://www.bafög.de/bafoeg/de/antrag-stellen/antrag-stellen_node.html",
    ]
    
    print("=== BAföG Web Scraper ===")
    print("This will scrape content from the provided URLs.")
    print("Note: Make sure you have permission to scrape these websites.\n")
    
    scraper.scrape_urls(urls)


if __name__ == "__main__":
    main()
