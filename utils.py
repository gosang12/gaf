import os, json
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

USER_DATA_FILE = "user_data.json"
HISTORY_DIR = "history"

def init_user():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({"credits": 3, "history": []}, f)

def load_user():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_user(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f)

def save_image(img_url, prompt):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    os.makedirs(HISTORY_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{HISTORY_DIR}/{timestamp}.png"
    img.save(filename)

    data = load_user()
    data["history"].append({"path": filename, "prompt": prompt})
    save_user(data)
    return filename
