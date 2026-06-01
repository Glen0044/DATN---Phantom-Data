
import logging
from datetime import timedelta
import pandas as pd
import config

# Cấu hình hiển thị log ra màn hình console để tiện theo dõi tiến độ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("cleaner")


def _validate_schema(df: pd.DataFrame, stage: str) -> None:
    """Kiểm tra cấu trúc (schema) dữ liệu sau mỗi bước xử lý."""
    null_counts = df.isnull().sum()
    null_cols   = null_counts[null_counts > 0]
    if not null_cols.empty:
        logger.warning("[%s] Các cột còn chứa giá trị rỗng (Null): %s", stage, null_cols.to_dict())
    logger.info("[%s] Kích thước bảng dữ liệu (Shape): %s", stage, df.shape)


def clean_basic_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa tên cột, xóa cột thừa không phân tích và lọc lỗi logic thời gian.
    """
    logger.info("Bước 1 — Chuẩn hóa tên cột và xóa các trường thừa...")

    # Đưa về chữ thường, thay khoảng trắng và dấu chấm thành dấu gạch dưới (_)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace(".", "_", regex=False)
    )

    # Loại bỏ các cột rác hoặc các cột trùng lặp thông tin
    junk_cols = ["row_id", "记录数", "weeknum", "market2", "year"]
    df.drop(columns=[c for c in junk_cols if c in df.columns], inplace=True, errors="ignore")

    logger.info("Bước 2 — Đồng bộ định dạng ngày tháng & Lọc lỗi logic...")
    # Ép kiểu dữ liệu ngày tháng sang Datetime chuẩn
    df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')
    df["ship_date"]  = pd.to_datetime(df["ship_date"], errors='coerce')

    # Loại bỏ các dòng lỗi hệ thống: Ngày giao hàng trước ngày đặt hàng
    invalid = (df["ship_date"] < df["order_date"]).sum()
    if invalid > 0:
        logger.warning("Phát hiện lỗi logic: Loại bỏ %d dòng có Ship Date < Order Date.", invalid)
        df = df[df["ship_date"] >= df["order_date"]].copy()

    # Gộp/loại bỏ trùng lặp nghiệp vụ (Một đơn hàng trùng mã sản phẩm)
    before = len(df)
    df = df.sort_values("order_date").drop_duplicates(
        subset=["order_id", "product_id"], keep="last"
    )
    removed = before - len(df)
    if removed > 0:
        logger.warning("Đã xử lý gộp %d dòng trùng lặp mã (Order ID + Product ID).", removed)

    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Xử lý các ô bị trống dữ liệu (Missing Values)."""
    logger.info("Bước 3 — Điền giá trị thiếu cho các trường dữ liệu...")

    # Xử lý cột mã bưu điện nếu có dòng trống
    if "postal_code" in df.columns:
        df["postal_code"] = df["postal_code"].fillna("00000")
        
    # Xử lý ép kiểu dữ liệu số và điền giá trị 0 nếu bị Null
    numeric_cols = ["sales", "quantity", "discount", "profit", "shipping_cost"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    _validate_schema(df, "handle_missing")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo thêm các biến/cột đặc trưng mới phục vụ vẽ biểu đồ nâng cao."""
    logger.info("Bước 4 — Thiết lập các thuộc tính bổ sung (Feature Engineering)...")

    # Tính Biên lợi nhuận (Tránh lỗi chia cho 0 bằng cách thay thế sales = 0 thành NaN)
    df["profit_margin"]   = df["profit"] / df["sales"].replace(0, float("nan"))
    df["profit_margin"]   = df["profit_margin"].fillna(0.0)
    
    # Tính số ngày chờ giao hàng thực tế
    df["ship_delay_days"] = (df["ship_date"] - df["order_date"]).dt.days
    
    # Trích xuất Năm và Quý đặt hàng phục vụ phân tích tăng trưởng YoY, QoQ
    df["order_year"]      = df["order_date"].dt.year
    df["order_quarter"]   = df["order_date"].dt.to_period("Q").astype(str)

    _validate_schema(df, "engineer_features")
    return df


def create_cohort_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo các trường dữ liệu phục vụ phân tích tỷ lệ giữ chân khách hàng (Cohort Analysis)."""
    logger.info("Bước 5 — Xây dựng thuộc tính phân tích nhóm khách hàng (Cohort)...")

    df["order_month"]  = df["order_date"].dt.to_period("M")
    
    # Tìm tháng đầu tiên phát sinh giao dịch của từng khách hàng
    df["cohort_month"] = (
        df.groupby("customer_id")["order_date"]
        .transform("min")
        .dt.to_period("M")
    )
    
    # Tính khoảng cách số tháng từ lần mua đầu tiên đến đơn hàng hiện tại
    df["cohort_index"] = (df["order_month"] - df["cohort_month"]).apply(lambda x: x.n)

    _validate_schema(df, "create_cohort_features")
    return df


def calculate_rfm_base(df: pd.DataFrame) -> pd.DataFrame:
    """Tính toán bộ chỉ số phân khúc khách hàng RFM (Recency, Frequency, Monetary)."""
    logger.info("Bước 6 — Tổng hợp và tính toán chỉ số RFM Base...")

    # Ngày chốt dữ liệu = Ngày có đơn hàng cuối cùng trong hệ thống + số ngày offset
    snapshot = df["order_date"].max() + timedelta(days=config.SNAPSHOT_DATE_OFFSET)

    rfm = df.groupby("customer_id").agg(
        recency   = ("order_date",  lambda x: (snapshot - x.max()).days),
        frequency = ("order_id",    "nunique"),
        monetary  = ("sales",       "sum"),
    ).reset_index()

    logger.info(
        "Kết quả RFM: Tổng số %d khách hàng | Recency TB: %.0f ngày | Đóng góp (Monetary) TB: %.0f $",
        len(rfm), rfm["recency"].mean(), rfm["monetary"].mean(),
    )
    return rfm


def run_all() -> None:
    """Hàm tổng điều phối chạy toàn bộ hệ thống pipeline."""
    logger.info("=== BẮT ĐẦU CHẠY PIPELINE LÀM SẠCH DỮ LIỆU ===")
    try:
        # Hỗ trợ đọc file với các định dạng mã hóa ký tự khác nhau để tránh lỗi tiếng Trung/ký tự lạ
        try:
            df = pd.read_csv(config.RAW_DATA_PATH, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(config.RAW_DATA_PATH, encoding="latin1")
            
        logger.info("Đọc thành công file dữ liệu gốc: %d dòng, %d cột.", *df.shape)

        # Chạy tuần tự qua các bước phân tích
        df = clean_basic_anomalies(df)
        df = handle_missing(df)
        df = engineer_features(df)
        df = create_cohort_features(df)

        # Lưu file dữ liệu tổng thể đã làm sạch
        cleaned_path = config.CLEANED_DIR / "superstore_cleaned.csv"
        df.to_csv(cleaned_path, index=False, encoding="utf-8-sig")
        logger.info("Đã xuất file dữ liệu sạch: %s (%d dòng)", cleaned_path, len(df))

        # Lưu file tổng hợp chỉ số RFM
        rfm = calculate_rfm_base(df)
        rfm_path = config.CLEANED_DIR / "rfm_base.csv"
        rfm.to_csv(rfm_path, index=False, encoding="utf-8-sig")
        logger.info("Đã xuất file phân tích phân khúc khách hàng: %s", rfm_path)

        logger.info("=== HỆ THỐNG HOÀN THÀNH LÀM SẠCH VÀ SẴN SÀNG ĐỂ PHÂN TÍCH ===")

    except FileNotFoundError:
        logger.error("Không tìm thấy file dữ liệu đầu vào tại đường dẫn: %s. Vui lòng kiểm tra lại vị trí file csv.", config.RAW_DATA_PATH)
    except Exception as exc:
        logger.exception("Đã xảy ra lỗi hệ thống nghiêm trọng ngoài dự kiến: %s", exc)


if __name__ == "__main__":
    run_all()