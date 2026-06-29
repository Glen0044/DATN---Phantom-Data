import pandas as pd

# Đọc file
df = pd.read_csv(r'D:\DATN\DATN---Phantom-Data\Dataset\superstore.csv', encoding='cp1252', encoding_errors='replace')
# ── Bước 1: Đổi tên cột cho dễ dùng 
df.rename(columns={
    'Nh\xf3m S?n ph?m'          : 'Category',
    'Th\xe0nh ph?'              : 'City',
    'Qu?c Gia'               : 'Country',
    'M\xe3 kh\xe1ch h\xe0ng duy nh?t' : 'Customer_ID',
    'T\xeaan kh\xe1ch h\xe0ng'         : 'Customer_Name',
    'M?c gi?m gi\xe1 \xe1p d?ng'   : 'Discount',
    'Th? tr??ng'             : 'Market',
    '记录数'                  : 'Record_Count',
    'Ng\xe0y ??t h\xe0ng'          : 'Order_Date',
    'M\xe3 ??n h\xe0ng duy nh?t'   : 'Order_ID',
}, inplace=True)

# ── Bước 2: Xóa cột không cần thiết
df.drop(columns=['Record_Count', 'weeknum', 'Market2', 'Row.ID'], errors='ignore', inplace=True)

# ── Bước 3: Xử lý ngày tháng
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Ship.Date']  = pd.to_datetime(df['Ship.Date'],  errors='coerce')

# ── Bước 4: Xóa dòng trùng lặp 
df.drop_duplicates(subset=['Order_ID', 'Product.ID'], inplace=True)
print(f"Sau khi xóa trùng: {df.shape}")

# ── Bước 5: Xóa dòng có giá trị âm vô lý
df = df[df['Sales'] > 0]
df = df[df['Quantity'] > 0]

# ── Bước 6: Reset index 
df.reset_index(drop=True, inplace=True)

# ── Xuất file sạch 
df.to_csv('superstore_cleaned.csv', index=False, encoding='utf-8-sig')
print(f"Dữ liệu sau làm sạch: {df.shape}")
print("✅ Xuất file thành công!")