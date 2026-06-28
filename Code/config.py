import os
from pathlib import Path

# Thư mục gốc của dự án
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent

# Đường dẫn đến file dữ liệu thô đầu vào
RAW_DATA_PATH = Path("D:/DATN/DATN---Phantom-Data/Dataset/superstore.csv")

# --- CẬP NHẬT ĐƯỜNG DẪN LƯU THEO Ý BẠN TẠI ĐÂY ---
# Hệ thống sẽ tạo và lưu vào thư mục "Data dự án/cleaned"
CLEANED_DIR = BASE_DIR / "Data dự án" / "cleaned"

# Tự động tạo toàn bộ chuỗi thư mục lồng nhau nếu chưa tồn tại
os.makedirs(CLEANED_DIR, exist_ok=True)

# --- ĐƯỜNG DẪN CÁC FILE ĐẦU RA ---
# Định dạng CSV
CLEANED_CSV_PATH = CLEANED_DIR / "superstore_cleaned.csv"
RFM_CSV_PATH      = CLEANED_DIR / "rfm_base.csv"

# Định dạng Excel (.xlsx)
CLEANED_XLSX_PATH = CLEANED_DIR / "superstore_cleaned.xlsx"
RFM_XLSX_PATH     = CLEANED_DIR / "rfm_base.xlsx"

# Số ngày cộng thêm sau ngày đặt hàng cuối cùng để làm ngày chốt tính RFM
SNAPSHOT_DATE_OFFSET = 1