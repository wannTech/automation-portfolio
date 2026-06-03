from dotenv import load_dotenv
import os

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = "appS1KfZch34nInvu"
TABLE_NAME = "Table 1"

EMAIL_PENGIRIM = os.getenv("EMAIL_PENGIRIM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

from pyairtable import Api
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def kirim_email(nama, email_penerima, pesan):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_PENGIRIM
    msg["To"] = email_penerima
    msg["Subject"] = "Terima kasih sudah menghubungi kami!"
    
    isi = f"""
Halo {nama},

Terima kasih sudah menghubungi kami!

Pesan kamu: "{pesan}"

Kami akan segera membalas dalam 1x24 jam.

Salam,
Tim Kami
"""
    msg.attach(MIMEText(isi, "plain"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_PENGIRIM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_PENGIRIM, email_penerima, msg.as_string())

def proses_leads():
    api = Api(AIRTABLE_TOKEN)
    table = api.table(BASE_ID, TABLE_NAME)
    
    # Ambil semua lead dengan status "baru"
    records = table.all(formula="status='baru'")
    
    if not records:
        print("Tidak ada lead baru.")
        return
    
    print(f"Ditemukan {len(records)} lead baru.")
    
    for record in records:
        fields = record["fields"]
        nama = fields.get("nama", "")
        email = fields.get("email", "")
        pesan = fields.get("pesan", "")
        record_id = record["id"]
        
        if not email:
            print(f"Skip {nama} — email kosong")
            continue
        
        # Kirim email balasan
        kirim_email(nama, email, pesan)
        print(f"Email terkirim ke {nama} ({email})")
        
        # Update status jadi "terkirim"
        table.update(record_id, {"status": "terkirim"})
        print(f"Status {nama} diupdate ke 'terkirim'")

# Jalanin
proses_leads()