#!/usr/bin/env python3
"""
Create knowledge base index for browser-side citations
Extracts keywords and metadata from each TXT file for client-side matching
"""
import os
import json
import re
from pathlib import Path


def extract_keywords(text, filename):
    """Extract relevant keywords from text"""
    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Common BAföG-related keywords to search for (German and English)
    keywords = []
    
    # Extract from filename (more relevant)
    name_parts = filename.replace('.txt', '').replace('-', ' ').replace('_', ' ')
    keywords.extend(name_parts.split())
    
    # Extract key terms from content (German)
    german_terms = [
        'bafög', 'förderung', 'antrag', 'student', 'studium', 'ausbildung',
        'einkommen', 'eltern', 'vermögen', 'rückzahlung', 'höhe', 'betrag',
        'altersgrenze', 'ausland', 'darlehen', 'zuschuss', 'bedarfssatz',
        'studienstarthilfe', 'studienabschluss', 'formblatt', 'amt',
        'förderungsdauer', 'förderungshöchstdauer', 'fachrichtung',
        'flexibilitätssemester', 'leistungsbescheinigung'
    ]
    
    # Add English equivalents for better international support
    english_terms = [
        'funding', 'application', 'study', 'education', 'income',
        'parents', 'assets', 'repayment', 'amount', 'age limit',
        'abroad', 'loan', 'grant', 'form', 'office'
    ]
    
    all_terms = german_terms + english_terms
    
    for term in all_terms:
        if term in text_lower:
            keywords.append(term)
    
    # Remove duplicates and return
    return list(set(keywords))


def create_knowledge_index():
    """Create searchable index of knowledge base files"""
    kb_dir = Path("./knowledge_base")
    url_mapping_file = kb_dir / "url_mapping.json"
    
    # Load URL mapping
    with open(url_mapping_file, 'r', encoding='utf-8') as f:
        url_mapping = json.load(f)
    
    index = []
    
    # Process each TXT file
    for filename, url in url_mapping.items():
        filepath = kb_dir / filename
        
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping")
            continue
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract first 200 characters as preview
        preview = content[:200].replace('\n', ' ').strip()
        if len(content) > 200:
            preview += "..."
        
        # Extract keywords
        keywords = extract_keywords(content, filename)
        
        # Create readable name
        display_name = filename.replace('.txt', '').replace('-', ' ').replace('_', ' ').title()
        
        index.append({
            'file': filename,
            'name': display_name,
            'url': url,
            'keywords': keywords,
            'preview': preview
        })
    
    # Save index
    output_file = kb_dir / "knowledge_index.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created knowledge index: {output_file}")
    print(f"  Indexed {len(index)} documents")
    print(f"  Total keywords: {sum(len(doc['keywords']) for doc in index)}")
    
    # Show a sample
    if index:
        print("\nSample entry:")
        sample = index[0]
        print(f"  File: {sample['file']}")
        print(f"  Name: {sample['name']}")
        print(f"  Keywords: {', '.join(sample['keywords'][:5])}...")
        print(f"  URL: {sample['url'][:60]}...")


if __name__ == "__main__":
    create_knowledge_index()
