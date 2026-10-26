import pandas as pd

df = pd.read_csv("/Users/marcotolol/binus/binus/AOL_DB/online_retail_data_with_names.csv")

jumlah_awal = len(df)

# Hapus baris yang StockCode-nya kosong
df = df.dropna(subset=["StockCode"])

# Hapus StockCode tanpa angka (POST, BANK CHARGES, DOT, GIFT, AMAZONFEE, dll - bukan produk asli)
df = df[df["StockCode"].astype(str).str.contains(r"\d")]

# ANOMALI #1: Missing Customer ID -  hapus baris yang tidak punya Customer ID
df = df.dropna(subset=["Customer ID"])

# ANOMALI #2: Missing Description - hapus baris yang tidak punya nama produk
df = df.dropna(subset=["Description"])

# ANOMALI #3: Exact duplicate - hapus baris yang isinya sama persis, sisakan satu
df = df.drop_duplicates(keep="first")

# ANOMALI #4: Negative Quantity
# -> hapus baris quantity negatif, KECUALI kalau invoice-nya cancelled (prefix "C").
#    Invoice ber-prefix "C" artinya transaksi dibatalkan/retur secara resmi, jadi
#    quantity negatifnya memang valid dan baris ini TETAP dipertahankan, tidak dihapus.
invoice_cancelled = df["Invoice"].astype(str).str.startswith("C")
quantity_negatif = df["Quantity"] < 0
df = df[~(quantity_negatif & ~invoice_cancelled)]

# ANOMALI #5: Invoice full alphabet
# hanya hapus kalau invoice murni huruf tanpa angka sama sekali
df = df[df["Invoice"].astype(str).str.contains(r"\d")]

# ANOMALI #6 & #7: Zero / Negative Price -> hapus baris dengan harga 0 atau negatif
df = df[df["Price"] > 0]

# ANOMALI #8: Customer di multiple countries
# -> hapus seluruh baris customer yang negaranya tidak konsisten
cust_country_count = df.groupby("Customer ID")["Country"].nunique()
customer_multi_country = cust_country_count[cust_country_count > 1].index
df = df[~df["Customer ID"].isin(customer_multi_country)]

# ANOMALI #9: Invoice has multiple timestamps
# -> tidak dihapus, selisih waktunya wajar (cuma 1-9 menit, proses checkout)
inv_time_count = df.groupby("Invoice")["InvoiceDate"].nunique()
invoice_multi_time = inv_time_count[inv_time_count > 1].index

# ANOMALI #10: Duplicate Invoice + StockCode -> hapus duplikatnya, sisakan satu
df = df.drop_duplicates(subset=["Invoice", "StockCode"], keep="first")

# ANOMALI #11: Multiple descriptions -> distandarisasi pakai deskripsi paling sering
most_common_desc = df.groupby("StockCode")["Description"].agg(lambda x: x.value_counts().idxmax())
df["Description"] = df["StockCode"].map(most_common_desc)

# ANOMALI #12: Multiple prices -> distandarisasi pakai harga PALING RENDAH per StockCode
harga_terendah = df.groupby("StockCode")["Price"].min()
df["Price"] = df["StockCode"].map(harga_terendah)

jumlah_akhir = len(df)
jumlah_terhapus = jumlah_awal - jumlah_akhir

print("Data awal:", jumlah_awal)
print("Data yang terhapus:", jumlah_terhapus)
print("Data setelah dibersihkan:", jumlah_akhir)

df.to_csv("data_clean_final.csv", index=False)