from functions_pdf import *
from functions_llm import *
from functions import *
import pymupdf

def lmm_runner(img_folder_path):
    for img_path in folder_path_to_files_paths(img_folder_path):
        response = run_llm(img_path)
        save_as_markdown(response.content, just_filename(img_path))
        print(f"Saved {just_filename(img_path)}")

def runner(pdf_path, start_page=None, end_page=None):
    doc = pymupdf.open(pdf_path)
    doc = pdf_select_pages(doc, start_page, end_page)

    img_output_folder = "data/pdf_screenshots"
    pdf_doc2screenshots(doc, img_output_folder)
    
    lmm_runner(img_output_folder)
    # clenup
    remove_folder_content(img_output_folder)
    out_folder_path="output"
    join_markdown_files(out_folder_path)

runner("data/ai1_Extracted102_105.pdf")