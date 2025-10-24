def extract_text_from_file(file_path):
    # Add logic for PDFs, images (OCR via easyocr if installed), etc.
    with open(file_path, 'r') as f:
        return f.read()