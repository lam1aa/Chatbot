#!/usr/bin/env python3
"""
Generate URL mapping from URLs.csv
Creates url_mapping.json with mappings for all TXT files
"""
import csv
import json
import os


def generate_url_mapping():
    """Parse URLs.csv and create url_mapping.json"""
    csv_file = "./knowledge_base/URLs.csv"
    json_file = "./knowledge_base/url_mapping.json"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    url_mapping = {}
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_name = row['file_name']
            url = row['url']
            doc_type = row['doc_type']
            
            # Only process TXT files
            if doc_type == 'TXT':
                # Add .txt extension if not present
                if not file_name.endswith('.txt'):
                    file_name = f"{file_name}.txt"
                
                url_mapping[file_name] = url
    
    # Write to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(url_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {json_file}")
    print(f"  Mapped {len(url_mapping)} TXT files to URLs")
    
    # Display a few examples
    print("\nExamples:")
    for i, (file_name, url) in enumerate(list(url_mapping.items())[:3]):
        print(f"  {file_name} -> {url}")
    
    if len(url_mapping) > 3:
        print(f"  ... and {len(url_mapping) - 3} more")


if __name__ == "__main__":
    generate_url_mapping()
