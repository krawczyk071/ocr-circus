from functions_pdf import *
from functions_llm import *
from functions import *
from pathlib import Path

BASE_DIR = Path().resolve() 

print(f"base app {BASE_DIR}")

def lmm_runner(img_folder_path):
    for img_path in folder_path_to_files_paths(img_folder_path):
        response = run_llm(img_path)

        out_folder_path=BASE_DIR.parent / "output"
        save_as_markdown(response.content, just_filename(img_path),out_folder_path)
        print(f"Saved {just_filename(img_path)}")

def runner(pdf_path, start_page=None, end_page=None):
    doc = open_pdf(pdf_path)
    doc = pdf_select_pages(doc, start_page, end_page)

    img_output_folder = BASE_DIR.parent / "data" / "pdf_screenshots"
    pdf_doc2screenshots(doc, img_output_folder)

    lmm_runner(img_output_folder)
    # clenup
    remove_folder_content(img_output_folder)
    out_folder_path=BASE_DIR.parent / "output"
    join_markdown_files(out_folder_path)



# runner("./data/ai1_Extracted102_105.pdf")