# Using the Web Scraper

## Quick Start

### Method 1: Interactive Scraping

```bash
python kb_manager.py scrape
```

Then enter URLs when prompted:

```
URL: https://www.bafög.de/bafoeg/de/home/home_node.html
URL: https://www.bafög.de/bafoeg/de/das-bafoeg/das-bafoeg_node.html
URL: [press Enter to finish]
```

### Method 2: Programmatic Scraping

Edit `scraper.py` and add your URLs to the `urls` list:

```python
urls = [
    "https://www.bafög.de/bafoeg/de/home/home_node.html",
    "https://www.bafög.de/bafoeg/de/das-bafoeg/das-bafoeg_node.html",
    "https://www.bafög.de/bafoeg/de/antrag-stellen/antrag-stellen_node.html",
    # Add more URLs here
]
```

Then run:

```bash
python scraper.py
```

## What Happens

1. The scraper downloads each webpage
2. Extracts the main text content (removes scripts, styles, navigation)
3. Saves each page as a `.txt` file in `knowledge_base/`
4. Updates `knowledge_base/url_mapping.json` with the source URLs
5. The chatbot will use this mapping to show sources in responses

## After Scraping

Always rebuild the vector database to include new content:

```bash
python kb_manager.py rebuild
python main.py
```

## Example URLs to Scrape

Here are some official BAföG URLs you might want to scrape:

```
https://www.bafög.de/bafoeg/de/home/home_node.html
https://www.bafög.de/bafoeg/de/das-bafoeg/das-bafoeg_node.html
https://www.bafög.de/bafoeg/de/antrag-stellen/antrag-stellen_node.html
https://www.bafög.de/bafoeg/de/welche-ausbildung-ist-foerderungsfaehig-/welche-ausbildung-ist-foerderungsfaehig-_node.html
https://www.bafög.de/bafoeg/de/wer-wird-gefoerdert/wer-wird-gefoerdert_node.html
https://www.bafög.de/bafoeg/de/wie-viel-bafoeg-gibt-es/wie-viel-bafoeg-gibt-es_node.html
```

## Tips

- Be respectful to the website (scraper includes 1-second delay between requests)
- Only scrape websites you have permission to scrape
- Check the website's `robots.txt` and terms of service
- The scraper removes navigation, scripts, and styling automatically
