import pandas as pd

df = pd.read_csv("/Users/marcotolol/binus/binus/AOL_DB/online_retail_data_with_names.csv")
jumlah_awal = len(df)

# StockCode kosong atau bukan produk asli (POST, BANK CHARGES, dll)
df = df.dropna(subset=["StockCode"])
df = df[df["StockCode"].astype(str).str.contains(r"\d")]

# Missing value
df = df.dropna(subset=["Customer ID"])
df = df.dropna(subset=["Description"])

# Duplikat persis
df = df.drop_duplicates(keep="first")

# Quantity negatif dihapus, kecuali invoice cancelled (prefix "C")
invoice_cancelled = df["Invoice"].astype(str).str.startswith("C")
quantity_negatif = df["Quantity"] < 0
df = df[~(quantity_negatif & ~invoice_cancelled)]

# Invoice tanpa angka
df = df[df["Invoice"].astype(str).str.contains(r"\d")]

# Harga 0 atau negatif
df = df[df["Price"] > 0]

# Customer dengan lebih dari satu negara
cust_country_count = df.groupby("Customer ID")["Country"].nunique()
customer_multi_country = cust_country_count[cust_country_count > 1].index
df = df[~df["Customer ID"].isin(customer_multi_country)]

# Duplikat Invoice + StockCode
df = df.drop_duplicates(subset=["Invoice", "StockCode"], keep="first")

# Standardisasi deskripsi (paling sering) dan harga (paling rendah)
most_common_desc = df.groupby("StockCode")["Description"].agg(lambda x: x.value_counts().idxmax())
df["Description"] = df["StockCode"].map(most_common_desc)

harga_terendah = df.groupby("StockCode")["Price"].min()
df["Price"] = df["StockCode"].map(harga_terendah)

jumlah_akhir = len(df)
print("Data awal:", jumlah_awal)
print("Data yang terhapus:", jumlah_awal - jumlah_akhir)
print("Data setelah dibersihkan:", jumlah_akhir)

df.to_csv("data_clean_final.csv", index=False)