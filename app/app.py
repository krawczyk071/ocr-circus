from functions_pdf import *
from functions_llm import *
from functions import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

print(f"base app {BASE_DIR}")

def lmm_runner(img_folder_path,chat_model):

    current_time=get_current_time_str()
    out_folder_path = BASE_DIR / "output" / chat_model / current_time
    Path(out_folder_path).mkdir(exist_ok=True, parents=True)

    for img_path in folder_path_to_files_paths(img_folder_path):
        response = run_llm(img_path, chat_model)

        save_as_markdown(response.content, just_filename(img_path),out_folder_path)
        print(f"Saved {just_filename(img_path)}")

    return out_folder_path

def runner(pdf_path, start_page=None, end_page=None,chat_model='gpt4omini'):
    doc = open_pdf(pdf_path)
    doc = pdf_select_pages(doc, start_page, end_page)

    # make screenshots of each page
    img_output_folder = BASE_DIR / "data" / "pdf_screenshots"
    pdf_doc2screenshots(doc, img_output_folder)

    # run LMM
    out_folder_path = lmm_runner(img_output_folder,chat_model)

    # clenup
    remove_folder_content(img_output_folder)

    # join markdown files
    # out_folder_path=BASE_DIR / "output" / chat_model

    join_markdown_files(out_folder_path)


runner("./data/ai1_Extracted102_105.pdf",1,1)