import pandas as pd

# Baca file CSV — telepon dibaca sebagai teks
df = pd.read_csv("data_kotor.csv", dtype={"telepon": str})

print("=== DATA SEBELUM DIBERSIHKAN ===")
print(df)
print(f"\nJumlah baris: {len(df)}")

# 1. Hapus baris yang nama-nya kosong
df = df.dropna(subset=["nama"])

# 2. Rapiin huruf
df["nama"] = df["nama"].str.strip().str.title()
df["kota"] = df["kota"].str.strip().str.title()
df["email"] = df["email"].str.strip().str.lower()

# 3. Hapus duplikat
df = df.drop_duplicates(subset=["nama", "email"], keep="first")

# 4. Isi kolom kosong
df["telepon"] = df["telepon"].fillna("Tidak Ada")
df["kota"] = df["kota"].fillna("Tidak Ada")
df["email"] = df["email"].fillna("Tidak Ada")

# 5. Reset index
df = df.reset_index(drop=True)

print("\n=== DATA SETELAH DIBERSIHKAN ===")
print(df)
print(f"\nJumlah baris: {len(df)}")

df.to_csv("data_bersih.csv", index=False)
print("\nFile disimpan ke data_bersih.csv")