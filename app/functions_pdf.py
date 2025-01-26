import pymupdf
from PIL import Image
from functions import *

# doc = pymupdf.open(pdf_file) # open a document

def pdf_select_pages(doc, start_page, end_page):

    if not start_page:
        start_page = 1
    if not end_page:
        end_page = doc.page_count

    doc.select(list(range(start_page-1, end_page))) # select the 1st & 2nd page of the document
    
    return doc


#Screenshots

def pdf_doc2screenshots(doc, output_folder="../data/pdf_screenshots", zoom_x=2.0, zoom_y=2.0):  # zoom increases resolution
    ensure_folder_exists(output_folder)
    # get doc filename
    fname = just_filename(doc.name) 

    try:
        
        mat = pymupdf.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        for page_num in range(doc.page_count):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=mat) # render page to an image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(f"{output_folder}/{fname}_p{page_num + 1}.png")
        
        return f"Screenshots saved to {output_folder}"
    except pymupdf.fitz.FileNotFoundError:
        return "Error: PDF file not found."
    except Exception as e:
        return f"An error occurred: {e}"

