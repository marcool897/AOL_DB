import pandas as pd

df = pd.read_csv("/Users/marcotolol/binus/binus/AOL_DB/online_retail_data_with_names.csv")
jumlah_awal = len(df)


# 1. Hapus data kosong
df = df.dropna(subset=["StockCode", "Customer ID", "Description"])


# 2. Hapus StockCode yang bukan produk (POST, BANK CHARGES, dll)
punya_angka = df["StockCode"].astype(str).str.contains(r"\d")
df = df[punya_angka]


# 3. Hapus duplikat persis
df = df.drop_duplicates(keep="first")


# 4. Hapus quantity negatif, kecuali invoice cancelled (diawali "C")
quantity_negatif = df["Quantity"] < 0
invoice_cancelled = df["Invoice"].astype(str).str.startswith("C")
harus_dihapus = quantity_negatif & ~invoice_cancelled
df = df[~harus_dihapus]


# 5. Hapus invoice yang tidak mengandung angka
invoice_punya_angka = df["Invoice"].astype(str).str.contains(r"\d")
df = df[invoice_punya_angka]


# 6. Hapus harga 0 atau negatif
harga_valid = df["Price"] > 0
df = df[harga_valid]


# 7. Hapus customer yang punya lebih dari satu negara
jumlah_negara = df.groupby("Customer ID")["Country"].nunique()
customer_bermasalah = jumlah_negara[jumlah_negara > 1].index
df = df[~df["Customer ID"].isin(customer_bermasalah)]


# 8. Hapus duplikat Invoice + StockCode
df = df.drop_duplicates(subset=["Invoice", "StockCode"], keep="first")


# 9. Standardisasi Description (paling sering muncul)
deskripsi_terbaik = df.groupby("StockCode")["Description"].agg(
    lambda x: x.value_counts().idxmax()
)
df["Description"] = df["StockCode"].map(deskripsi_terbaik)


# 10. Standardisasi Price (paling rendah)
harga_terendah = df.groupby("StockCode")["Price"].min()
df["Price"] = df["StockCode"].map(harga_terendah)


# Hasil
jumlah_akhir = len(df)
print("Data awal:", jumlah_awal)
print("Data yang terhapus:", jumlah_awal - jumlah_akhir)
print("Data setelah dibersihkan:", jumlah_akhir)

df.to_csv("data_clean_final.csv", index=False)