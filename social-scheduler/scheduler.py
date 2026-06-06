import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import schedule
import time

# Setup Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Buka sheet
sheet = client.open("Social Scheduler").sheet1

def cek_dan_posting():
    sekarang = datetime.now().strftime("%H:%M")
    print(f"Cek jadwal: {sekarang}")
    
    records = sheet.get_all_records()
    
    for i, row in enumerate(records):
        konten = row["konten"]
        jam = row["jam_posting"]
        status = row["status"]
        
        if status == "pending" and jam == sekarang:
            print(f"Posting: {konten}")
            
            # Update status jadi "posted"
            sheet.update_cell(i + 2, 3, "posted")
            print(f"Status diupdate ke posted")

# Jalanin cek tiap menit
schedule.every(1).minutes.do(cek_dan_posting)

print("Scheduler jalan! Tekan CTRL+C untuk stop.")
cek_dan_posting()

while True:
    schedule.run_pending()
    time.sleep(30)