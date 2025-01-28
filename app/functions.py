import os
import shutil
import datetime

def folder_path_to_files_paths(folder_path: str) -> list[str]:
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    file_paths.sort()
    
    return file_paths

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"Folder '{folder_path}' created."
    else:
        return f"Folder '{folder_path}' already exists."


def remove_folder_content(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)  # Recreate the folder after deleting its content
            return f"All contents of the folder '{folder_path}' have been removed."
        else:
            return f"Folder '{folder_path}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"
    
def just_filename(path_string):
    name = os.path.splitext(os.path.basename(path_string))[0]
    return name

def join_markdown_files(folder_path):
    
    output_file = folder_path.parent / f'merged_{folder_path.stem}.md'

    with open(output_file, 'w') as outfile:

        mds_list = sorted(os.listdir(folder_path))
        for filename in mds_list:
            if filename.endswith('.md'):
                with open(os.path.join(folder_path, filename), 'r') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")  # Add a newline between files
                # print(f"Added {filename}")

def get_current_time_str():        
        current_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        return current_time