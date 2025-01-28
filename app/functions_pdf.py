import pymupdf
from PIL import Image
from functions import *

# doc = pymupdf.open(pdf_file) # open a document
def open_pdf(pdf_path):
    if isinstance(pdf_path, str):
        doc = pymupdf.open(pdf_path)
    else:
        file_contents = pdf_path.read()
        doc = pymupdf.open(stream=file_contents, filetype="pdf")
    return doc

def pdf_select_pages(doc, start_page, end_page):

    if not start_page or start_page < 1:
        start_page = 1
    if not end_page or end_page > doc.page_count:
        end_page = doc.page_count
    if end_page and end_page < start_page:
        end_page = start_page

    doc.select(list(range(start_page-1, end_page))) # select the 1st & 2nd page of the document
    
    return doc


#Screenshots

def pdf_doc2screenshots(doc, output_folder, zoom_x=2.0, zoom_y=2.0):  # zoom increases resolution
    ensure_folder_exists(output_folder)
    # get doc filename
    if doc.name:
        fname = just_filename(doc.name) 
    else:
        current_time = get_current_time_str()
        fname = f"upload_{current_time}"

    try:
        
        mat = pymupdf.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        for page_num in range(doc.page_count):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=mat) # render page to an image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            fnumb = str(page_num + 1).zfill(3)
            img.save(f"{output_folder}/{fname}_p{fnumb}.png")
        
        return f"Screenshots saved to {output_folder}"
    except pymupdf.fitz.FileNotFoundError:
        return "Error: PDF file not found."
    except Exception as e:
        return f"An error occurred: {e}"

