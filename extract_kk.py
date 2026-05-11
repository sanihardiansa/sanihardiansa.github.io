import pdfplumber
import json
import re

pdf_path = '/Users/cinot/MyWork/RT04/2419_001.pdf'

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total halaman: {len(pdf.pages)}")
    
    for i, page in enumerate(pdf.pages):
        print(f"\n=== Halaman {i+1} ===")
        text = page.extract_text()
        print(text)
        print("\n" + "="*50)
