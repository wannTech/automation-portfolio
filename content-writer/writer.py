from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_konten(nama_produk, deskripsi, harga):
    prompt = f"""Buatkan konten marketing untuk produk berikut:

Nama produk: {nama_produk}
Deskripsi: {deskripsi}
Harga: {harga}

Buatkan dalam format berikut:

CAPTION INSTAGRAM:
[caption menarik dengan emoji dan hashtag, max 150 kata]

EMAIL PROMO:
[subject email]
[isi email yang persuasif, max 100 kata]

Gunakan bahasa Indonesia yang menarik dan persuasif."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("=== AUTO CONTENT WRITER ===\n")
    
    nama = input("Nama produk: ")
    deskripsi = input("Deskripsi singkat: ")
    harga = input("Harga: ")
    
    print("\nGenerating konten...\n")
    hasil = generate_konten(nama, deskripsi, harga)
    print(hasil)
    
    # Simpan ke file
    with open("hasil_konten.txt", "w", encoding="utf-8") as f:
        f.write(f"Produk: {nama}\n\n")
        f.write(hasil)
    
    print("\nKonten disimpan ke hasil_konten.txt")