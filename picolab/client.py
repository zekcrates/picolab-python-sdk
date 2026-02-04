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

    if not os.path.exists(os.path.join(cwd, "picolab.yaml")):
        return {"success": False, "message": "No 'picolab.yaml' found. Are you in the right folder?"}
    
    zip_filename = "pico_submission.zip"

    with zipfile.ZipFile(zip_filename ,'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(cwd):
            # we will ignore some folders here 
            
            for file in files:
                if file == zip_filename :
                    continue
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, cwd)
                zipf.write(local_path, rel_path)

    try:
        with open(zip_filename, 'rb') as f:
            headers = {"Authorization": api_key}
            files = {"file": f}

            response = requests.post(f"{SERVER_URL}/push", headers=headers, files=files)

            if response.status_code == 200:
                return {"success": True, "data": response.json()} 
            elif response.status_code == 401:
                return {"success": False, "message": "Invalid API Key. Try 'picolab login' again."}
            else:
                return {"success": False, "message": f"Server Error ({response.status_code}): {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Could not connect to Picolab Server."}
    except Exception as e:
        return {"success": False, "message": f"Client Error: {str(e)}"}
    finally:
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
def verify_key(api_key: str):
    """
    Hits the server's /login endpoint to check if the key is valid.
    Returns: (True, username) OR (False, error_message)
    """

    print(f"Verifying key with {SERVER_URL}...")

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