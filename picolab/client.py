import shutil
import os
import time
from pathlib import Path
import zipfile 
import requests
import io 


SERVER_URL = "http://127.0.0.1:8000"

# for - get project

def download_starter_project(project_name: str, api_key:str):
    target_dir = Path.cwd()/project_name
    if target_dir.exists():
        return False, f"Folder '{project_name}' already exists. Delete it first."
    print(f"Connecting to {SERVER_URL}...")

    try:
        headers = {"Authorization": api_key}
        response = requests.get(f"{SERVER_URL}/get", params={"project_name": project_name}
                                , headers=headers)

        if response.status_code == 404:
            return False, f"Project '{project_name}' does not exist on the server."
        if response.status_code != 200:
            return False, f"Server Error: {response.text}"
        print("Extracting files...")
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(target_dir)

        return True, f"Downloaded to {target_dir}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to server. Is it running?"
    
    
def upload_project(api_key: str):
    cwd = os.getcwd()
    project_slug = os.path.basename(cwd)

    zip_name = "picolab_upload"
    shutil.make_archive(zip_name, 'zip', cwd)
    zip_file = f"{zip_name}.zip"



def verify_key(api_key: str):
    """
    Hits the server's /login endpoint to check if the key is valid.
    Returns: (True, username) OR (False, error_message)
    """

    print(f"🌍 Verifying key with {SERVER_URL}...")

    try:
        payload = {"apikey": api_key}
        response = requests.post(f"{SERVER_URL}/login", json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return True, data.get("user", "Unknown User")
            else:
                return False, data.get("message" , "Invalid key")
        elif response.status_code== 401:
            return False, "Key Rejected: Invalid Api Key"
        
        else:
            return False, f"Server Error: {response.status_code}"
        
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to server. Is it running?"