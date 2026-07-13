import logging
import pandas as pd
import config

# Cấu hình log hiển thị tiến độ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("eda_explorer")


def explore_raw_data():
    logger.info("=== BẮT ĐẦU QUY TRÌNH KHÁM PHÁ DỮ LIỆU GỐC (EDA) ===")
    try:
        # Hỗ trợ đọc file tránh lỗi bảng mã ký tự lạ
        try:
            df = pd.read_csv(config.RAW_DATA_PATH, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(config.RAW_DATA_PATH, encoding="latin1")

        print("\n" + "="*25)
        print(" BÁO CÁO DỮ LIỆU THÔ")
        print("="*25)

        # 1. Kiểm tra kích thước tổng quan
        print(f"\n[1] Tổng số dòng: {df.shape[0]} | Tổng số cột: {df.shape[1]}")

        # 2. Kiểm tra các dòng bị trống (Missing Values)
        print("\n[2] Thống kê các cột bị khuyết thiếu dữ liệu (Null):")
        null_counts = df.isnull().sum()
        missing_cols = null_counts[null_counts > 0]
        if not missing_cols.empty:
            for col, val in missing_cols.items():
                pct = (val / len(df)) * 100
                print(f"    - Cột '{col}': Trống {val} dòng ({pct:.2f}%)")
        else:
            print("    -> Tuyệt vời: Không có cột nào bị trống dữ liệu.")

        # 3. Kiểm tra trùng lặp nghiệp vụ hoàn toàn
        print("\n[3] Kiểm tra trùng lặp dữ liệu:")
        duplicate_count = df.duplicated().sum()
        print(f"    - Số lượng dòng bị trùng lặp 100% tất cả các trường: {duplicate_count} dòng")

        # 4. Kiểm tra lỗi logic thời gian (Ngày giao trước ngày đặt)
        print("\n[4] Kiểm tra lỗi logic hệ thống:")
        
        # Sửa đổi: Tìm kiếm thông minh bằng từ khóa 'order' và 'ship' trong tên cột
        order_col = [c for c in df.columns if 'order' in c.lower()]
        ship_col = [c for c in df.columns if 'ship' in c.lower()]
        
        if order_col and ship_col:
            order_dt = pd.to_datetime(df[order_col[0]], errors='coerce')
            ship_dt = pd.to_datetime(df[ship_col[0]], errors='coerce')
            logic_errors = (ship_dt < order_dt).sum()
            print(f"    - Số dòng có ngày giao hàng trước ngày đặt hàng (Ship Date < Order Date): {logic_errors} dòng")
        else:
            print("    - Không tìm thấy cột ngày tháng tương ứng để kiểm tra logic.")

        print("\n" + "="*50)
        logger.info("=== KẾT THÚC BƯỚC KHÁM PHÁ — Dữ liệu đã sẵn sàng để lập quy trình làm sạch ===")

    except FileNotFoundError:
        logger.error(f"Không tìm thấy file 'superstore.csv' tại đường dẫn: {config.RAW_DATA_PATH}")
    except Exception as e:
        logger.exception(f"Đã xảy ra lỗi trong quá trình khám phá dữ liệu: {e}")


if __name__ == "__main__":
    explore_raw_data()