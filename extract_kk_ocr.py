from pdf2image import convert_from_path
import pytesseract
import json
import re

pdf_path = '/Users/cinot/MyWork/RT04/2419_001.pdf'

try:
    images = convert_from_path(pdf_path)
    print(f"Total halaman: {len(images)}")
    
    all_text = ""
    for i, image in enumerate(images):
        print(f"\n=== Halaman {i+1} ===")
        text = pytesseract.image_to_string(image, lang='ind')
        all_text += text + "\n\n"
        print(text)
        
    # Simpan hasil OCR
    with open('kk_ocr_result.txt', 'w') as f:
        f.write(all_text)
    print("\n\nHasil OCR disimpan ke kk_ocr_result.txt")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nCoba ekstrak sebagai gambar saja...")
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            im = page.to_image()
            im.save(f'kk_page_{i+1}.png')
            print(f"Halaman {i+1} disimpan sebagai kk_page_{i+1}.png")
