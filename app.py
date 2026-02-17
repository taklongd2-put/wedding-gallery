import os
import json
from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# Google Drive Setup
# =========================

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

info = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    info,
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)

# ใส่ Folder ID ของคุณตรงนี้
FOLDER_ID = "1wl9oajwsniXb6Cjh6NmQa61CzPvWVg1I"

# =========================
# Routes
# =========================

@app.route("/")
def index():
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType contains 'image/'",
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    images = [
        {
            "name": file["name"],
            "url": f"https://drive.google.com/uc?id={file['id']}"
        }
        for file in files
    ]

    return render_template("index.html", images=images)


@app.route("/slideshow")
def slideshow():
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType contains 'image/'",
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    images = [
        f"https://drive.google.com/uc?id={file['id']}"
        for file in files
    ]

    return render_template("slideshow.html", images=images)


# =========================
# Run App
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
