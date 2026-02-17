import os
from flask import Flask, render_template, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# 🔹 ใส่ Folder ID ของคุณ
FOLDER_ID = "1wl9oajwsniXb6Cjh6NmQa61CzPvWVg1I"

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# 🔹 ใช้ service-account.json ในโฟลเดอร์เดียวกับ app.py
credentials = service_account.Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)


def get_images():
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType contains 'image/' and trashed=false",
        fields="files(id, name, createdTime)",
        orderBy="createdTime desc",
        pageSize=500
    ).execute()

    files = results.get('files', [])
    images = []

    for f in files:
        images.append({
            "id": f["id"],
            "name": f["name"],
            # 🔥 ใช้ thumbnail แบบเสถียร
            "url": f"https://drive.google.com/thumbnail?id={f['id']}&sz=w1000",
            "download_url": f"https://drive.google.com/uc?export=download&id={f['id']}"
        })

    return images


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/images")
def api_images():
    return jsonify(get_images())


@app.route("/slideshow")
def slideshow():
    return render_template("slideshow.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
