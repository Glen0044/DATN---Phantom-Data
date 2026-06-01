import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent

# Đường dẫn đến file dữ liệu thô đầu vào
# Đảm bảo bạn đặt file 'superstore.csv' cùng thư mục hoặc sửa đường dẫn tại đây
RAW_DATA_PATH = BASE_DIR / "superstore.csv"

# Thư mục lưu kết quả sau khi làm sạch
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

# Tự động tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(CLEANED_DIR, exist_ok=True)

# Số ngày cộng thêm sau ngày đặt hàng cuối cùng để làm ngày chốt tính RFM (Mặc định: 1 ngày)
SNAPSHOT_DATE_OFFSET = 1