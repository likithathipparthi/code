import fitz  
from PIL import Image
import pytesseract
import io
import os
os.makedirs("output_images", exist_ok=True)
os.makedirs("output_pages", exist_ok=True)
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text
def split_pdf_into_pages(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        single_page_pdf = fitz.open()
        single_page_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
        output_filename = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
        single_page_pdf.save(output_filename)
        single_page_pdf.close()
        print(f"Page {page_num + 1} saved as {output_filename}")
def convert_pdf_pages_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_data = pix.pil_tobytes(format="png")
        img = Image.open(io.BytesIO(img_data))
        output_filename = os.path.join(output_folder, f"page_{page_num + 1}.png")
        img.save(output_filename)
        print(f"Page {page_num + 1} image saved as {output_filename}")
def extract_text_from_scanned_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_data = pix.pil_tobytes(format="png")
        img = Image.open(io.BytesIO(img_data))
        text += pytesseract.image_to_string(img) + "\n"
    return text
pdf_file = "/mnt/data/scanned.pdf"
extracted_text = extract_text_from_pdf(pdf_file)
print("Extracted text from PDF:", extracted_text)
split_pdf_into_pages(pdf_file, "output_pages")
convert_pdf_pages_to_images(pdf_file, "output_images")
extracted_text_from_images = extract_text_from_scanned_pdf(pdf_file)
print("Extracted text from scanned PDF via OCR:", extracted_text_from_images)