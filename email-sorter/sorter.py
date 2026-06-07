from groq import Groq
import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def kategoriin_email(subjek, isi):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """Kamu adalah email classifier. 
Kategorikan email ke salah satu dari: URGENT, INQUIRY, COMPLAINT, SPAM, INFO
Jawab HANYA dengan satu kata kategori, tidak lebih."""
            },
            {
                "role": "user",
                "content": f"Subject: {subjek}\n\nIsi: {isi[:500]}"
            }
        ]
    )
    return response.choices[0].message.content.strip()

def baca_email():
    print("Connecting ke Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    
    # Ambil 5 email terbaru yang belum dibaca
    _, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()[-5:]
    
    if not email_ids:
        print("Tidak ada email baru.")
        return
    
    print(f"Ditemukan {len(email_ids)} email baru.\n")
    
    hasil = []
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subjek = msg["subject"] or "No Subject"
        pengirim = msg["from"] or "Unknown"
        
        # Ambil isi email
        isi = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    isi = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
        else:
            isi = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
        
        # Kategoriin pake AI
        kategori = kategoriin_email(subjek, isi)
        
        print(f"📧 Dari: {pengirim}")
        print(f"📌 Subject: {subjek}")
        print(f"🏷️  Kategori: {kategori}")
        print("-" * 40)
        
        hasil.append({
            "dari": pengirim,
            "subjek": subjek,
            "kategori": kategori
        })
    
    mail.close()
    mail.logout()
    
    # Simpan hasil ke file
    with open("hasil_sorting.txt", "w", encoding="utf-8") as f:
        for item in hasil:
            f.write(f"Dari: {item['dari']}\n")
            f.write(f"Subject: {item['subjek']}\n")
            f.write(f"Kategori: {item['kategori']}\n")
            f.write("-" * 40 + "\n")
    
    print("\nHasil disimpan ke hasil_sorting.txt")

baca_email()