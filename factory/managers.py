import os

def get_real_dir(file_name: str):
    # Project root (current working directory)
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(PROJECT_ROOT, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return file_path
