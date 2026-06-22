from groq import Groq
import os
from flask import Flask, request
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")

app = Flask(__name__)

# Baca FAQ
with open("faq.txt", "r", encoding="utf-8") as f:
    FAQ = f.read()

# Setup Groq
client = Groq(api_key=GROQ_API_KEY)

def tanya_ai(pertanyaan):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""Kamu adalah customer service assistant yang ramah.
Jawab pertanyaan pelanggan berdasarkan FAQ berikut.
Kalau pertanyaan tidak ada di FAQ, bilang kamu tidak tahu dan sarankan untuk menghubungi admin.
Jawab dalam bahasa Indonesia yang ramah dan singkat.

FAQ:
{FAQ}"""
            },
            {
                "role": "user",
                "content": pertanyaan
            }
        ]
    )
    return response.choices[0].message.content

def kirim_telegram(chat_id, pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan}
    requests.post(url, data=payload)

def kirim_wa(nomor, pesan):
    url = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    payload = {"target": nomor, "message": pesan}
    requests.post(url, headers=headers, data=payload)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    pertanyaan = data["message"]["text"]
    print(f"Telegram - Pertanyaan: {pertanyaan}")
    jawaban = tanya_ai(pertanyaan)
    kirim_telegram(chat_id, jawaban)
    return "ok"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.json
    nomor = data.get("sender")
    pertanyaan = data.get("message")
    print(f"WA - Pertanyaan: {pertanyaan}")
    jawaban = tanya_ai(pertanyaan)
    kirim_wa(nomor, jawaban)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)