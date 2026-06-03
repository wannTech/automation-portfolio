import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

url = "https://books.toscrape.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def kirim_notif(pesan):
    token = "8955461804:AAHCY-s_9vXCN0F5g3NOZqSVNp3mWjB4SUg"
    chat_id = "6607149521"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan
    }
    requests.post(url, data=payload)

def ambil_harga():
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    buku_list = soup.find_all("article", class_="product_pod")
    
    hasil = []
    for buku in buku_list:
        nama = buku.find("h3").find("a")["title"]
        harga = buku.find("p", class_="price_color").text.strip()
        harga_angka = float(harga.replace("£", "").strip())
        hasil.append({"nama": nama, "harga": harga_angka})
    
    return hasil

def cek_perubahan(data_baru):
    file_ada = os.path.exists("harga.csv")
    
    # Kalau file belum ada, simpan dulu sebagai data awal
    if not file_ada:
        with open("harga.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nama", "harga", "waktu"])
            writer.writeheader()
            for item in data_baru:
                writer.writerow({
                    "nama": item["nama"],
                    "harga": item["harga"],
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
        print(f"TURUN! {nama}: £{harga_lama} -> £{harga_baru}")
        kirim_notif(f"HARGA TURUN!\n{nama}\nDari £{harga_lama} jadi £{harga_baru}")
        return

    # Baca data lama
    data_lama = {}
    with open("harga.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_lama[row["nama"]] = float(row["harga"])

    # Bandingkan harga
    print(f"\n=== Cek harga: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    ada_perubahan = False
    for item in data_baru:
        nama = item["nama"]
        harga_baru = item["harga"]
        if nama in data_lama:
            harga_lama = data_lama[nama]
            if harga_baru < harga_lama:
                print(f"TURUN! {nama}: £{harga_lama} -> £{harga_baru}")
                ada_perubahan = True
            elif harga_baru > harga_lama:
                print(f"Naik: {nama}: £{harga_lama} -> £{harga_baru}")
    
    if not ada_perubahan:
        print("Tidak ada perubahan harga.")

    # Update file CSV dengan data terbaru
    with open("harga.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nama", "harga", "waktu"])
        writer.writeheader()
        for item in data_baru:
            writer.writerow({
                "nama": item["nama"],
                "harga": item["harga"],
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

# Jalanin
data = ambil_harga()
cek_perubahan(data)

kirim_notif("Test notif dari Price Tracker bot!")