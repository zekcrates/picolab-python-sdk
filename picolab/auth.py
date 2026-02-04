from pathlib import Path
# Constants
APP_NAME = "picolab"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
CONFIG_FILE = CONFIG_DIR / "key"

def save_key(key: str):
    """Writes the API key to the user's config folder."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()
    
    with open(CONFIG_FILE, "w") as f:
        f.write(key)

def load_key():
    """Reads the API key. Returns None if not found."""
    if not CONFIG_FILE.exists():
        return None 
    with open(CONFIG_FILE, "r") as f:
        return f.read().strip()
def get_key_or_fail():
    key = load_key()
    if not key:
        raise FileNotFoundError("User is not logged in.")
    return key 
