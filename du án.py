import pandas as pd

# Đọc dữ liệu
df = pd.read_csv("D:/DATN/data/superstore.csv")


# Kiểm tra thông tin
print(df.info())
print(df.describe())

# Làm sạch
df = df.drop_duplicates()
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Lưu dữ liệu sạch
df.to_csv("data/interim/superstore_clean.csv", index=False)
