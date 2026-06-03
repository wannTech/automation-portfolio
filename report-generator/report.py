import pandas as pd
import requests
from datetime import datetime

# Konfigurasi Telegram
TOKEN = "8955461804:AAHCY-s_9vXCN0F5g3NOZqSVNp3mWjB4SUg"
CHAT_ID = "6607149521"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def buat_laporan():
    # Baca data
    df = pd.read_csv("penjualan.csv", encoding="latin1")
    
    # Hitung total pendapatan per baris
    df["total"] = df["jumlah"] * df["harga"]
    
    # Summary keseluruhan
    total_pendapatan = df["total"].sum()
    total_item = df["jumlah"].sum()
    
    # Produk terlaris
    terlaris = df.groupby("produk")["jumlah"].sum().idxmax()
    
    # Pendapatan per produk
    per_produk = df.groupby("produk")["total"].sum()
    
    # Tanggal hari ini
    hari_ini = datetime.now().strftime("%d %B %Y")
    
    # Susun pesan laporan
    pesan = f"""
📊 <b>LAPORAN PENJUALAN</b>
📅 {hari_ini}
━━━━━━━━━━━━━━━

📦 <b>Total Item Terjual:</b> {total_item} pcs
💰 <b>Total Pendapatan:</b> Rp {total_pendapatan:,.0f}
🏆 <b>Produk Terlaris:</b> {terlaris}

📋 <b>Pendapatan per Produk:</b>
"""
    for produk, total in per_produk.items():
        pesan += f"• {produk}: Rp {total:,.0f}\n"

    pesan += "\n━━━━━━━━━━━━━━━"
    pesan += "\n<i>Laporan otomatis by Price Tracker Bot</i>"
    
    return pesan

# Jalanin
laporan = buat_laporan()
print(laporan)
kirim_telegram(laporan)
print("\nLaporan terkirim ke Telegram!")