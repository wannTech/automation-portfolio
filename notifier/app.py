from flask import Flask, request, jsonify
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Konfigurasi Telegram
TELEGRAM_TOKEN = "8955461804:AAHCY-s_9vXCN0F5g3NOZqSVNp3mWjB4SUg"
TELEGRAM_CHAT_ID = "6607149521"

# Konfigurasi Email
EMAIL_PENGIRIM = "ayottrader@gmail.com"
EMAIL_PASSWORD = "hrlhvekcxqvqyync"
EMAIL_PENERIMA = "hermawan170303@gmail.com"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": pesan}
    requests.post(url, data=payload)

def kirim_email(subjek, pesan):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_PENGIRIM
    msg["To"] = EMAIL_PENERIMA
    msg["Subject"] = subjek
    msg.attach(MIMEText(pesan, "plain"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_PENGIRIM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_PENGIRIM, EMAIL_PENERIMA, msg.as_string())

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    nama = data.get("nama", "")
    email = data.get("email", "")
    pesan = data.get("pesan", "")

    notif = f"""
📬 LEAD BARU MASUK!
👤 Nama: {nama}
📧 Email: {email}
💬 Pesan: {pesan}
"""
    # Kirim ke Telegram
    kirim_telegram(notif)
    
    # Kirim ke Email
    kirim_email("Lead Baru Masuk!", notif)
    
    return jsonify({"status": "ok", "message": "Notifikasi terkirim!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)