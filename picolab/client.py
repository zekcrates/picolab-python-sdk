import shutil
import os
import time
from pathlib import Path

SERVER_URL = "http://127.0.0.1:8000"

# for - get project
def create_starter_project(project_name: str):
    path = Path.cwd()/project_name
    if path.exists():
        return False,"Folder already exists"

    path.mkdir()
    (path / "main.py").write_text("print('Build something tiny!')")
    (path / "README.md").write_text(f"# {project_name}\n\nRun 'picolab push' to test.")
    (path / "tests.py").write_text(f"# {project_name}\n\nRun 'picolab push' to test.")

    return True, str(path)
    

def upload_project(api_key: str):
    cwd = os.getcwd()
    project_slug = os.path.basename(cwd)

    zip_name = "picolab_upload"
    shutil.make_archive(zip_name, 'zip', cwd)
    zip_file = f"{zip_name}.zip"
