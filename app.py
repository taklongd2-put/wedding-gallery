import os
import json
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# Google Sheets Setup
# =========================

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# ดึง credentials จาก Environment Variable
info = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    info,
    scopes=SCOPES
)
SPREADSHEET_ID = "1TAeXgt_j7PhepauTIF2T-VR1bMPqigYXCHPJueLmiK8"
RANGE_NAME = "Sheet1!A:C"

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

# =========================
# Routes
# =========================

@app.route("/")
def index():
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    values = result.get("values", [])

    return render_template("index.html", values=values)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    message = request.form.get("message")

    body = {
        "values": [[name, message]]
    }

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    return redirect(url_for("index"))


# =========================
# Run App
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
