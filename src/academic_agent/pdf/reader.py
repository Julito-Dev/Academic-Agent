from pypdf import PdfReader
import re
import unicodedata
from collections import Counter


def extract_pages(route):
    reader = PdfReader(route)
    
    pages = []
    
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    
    return pages


def clean_headers_and_footers(pages):
    counter = Counter()
    
    for text in pages:
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        # First and last 3 lines of each page
        counter.update(lines[:3])
        counter.update(lines[-3:])
        
    #  Lines that appears at least 50% of the pages
    limit = len(pages) * 0.5
    
    repeated = {
        line for line, frecuency in counter.items()
        if frecuency >= limit
    }
    
    result = []
    
    for text in pages:
        lines = text.splitlines()
        
        lines = [
            l for l in lines
            if l.strip() not in repeated
        ]
        
        result.append("\n".join(lines))
    
    return result


def join_splitted_words(text):
    
    # Delete soft dashes
    text = text.replace("\u00ad", "")
    
    # Rebuild splitted words by line break
    text = re.sub(
        r"(?<=[a-záéíóúüñ])-\s*\n\s*(?=[a-záéíóúüñ])",
        "",
        text,
        flags=re.IGNORECASE
    )
    
    return text


def normalize_spaces(text):
    # Normalize Unicode Characters
    text = unicodedata.normalize("NFC", text)
    
    # Delete Final line Spaces
    text = re.sub(r"[ \t]+", " ", text)
    
    # Reduce excessive line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Delete spaces at the beginning and end
    text = text.strip()
    
    return text 

def clean_text(route):
    
    pages = extract_pages(route)
    
    pages = clean_headers_and_footers(pages)
    
    text = "\n\n".join(pages)
    
    text = join_splitted_words(text)
    text = normalize_spaces(text)
    
    return text
