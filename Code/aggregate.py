import logging
import pandas as pd
import numpy as np
import config 

logger = logging.getLogger("aggregate")











# 4. Hàm Phân tích Đa biến: Hiệu suất Vận chuyển & Logistics
def get_shipping_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích mối tương quan giữa Hình thức vận chuyển, Mức độ ưu tiên đơn hàng đối với chi phí và số ngày trễ.
    """
    logger.info("Phân tích đa biến: Đánh giá hiệu suất Logistics & Giao hàng...")
    
    shipping = df.groupby(['ship_mode', 'order_priority']).agg(
        avg_shipping_cost = ('shipping_cost', 'mean'),
        avg_delay_days    = ('ship_delay_days', 'mean'),
        total_orders      = ('order_id', 'nunique')
    ).reset_index()
    
    return shipping


# 5. Hàm Phân tích Đa biến Nâng cao: Ma trận Cohort (Cohort Retention Matrix)
def calculate_cohort_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xây dựng ma trận tỷ lệ giữ chân khách hàng qua các tháng (Customer Retention Rate).
    """
    logger.info("Phân tích nâng cao: Tính toán ma trận giữ chân khách hàng (Cohort Analysis)...")
    
    cohort_group = df.groupby(['cohort_month', 'cohort_index']).agg(
        unique_customers = ('customer_id', 'nunique')
    ).reset_index()
    
    cohort_matrix = cohort_group.pivot(
        index='cohort_month', 
        columns='cohort_index', 
        values='unique_customers'
    )
    
    cohort_size = cohort_matrix.iloc[:, 0]
    cohort_retention = cohort_matrix.divide(cohort_size, axis=0)
    
    return cohort_retention


# ──────────────────────────────────────────────────────────────
def run_all() -> None:
    """Chạy toàn bộ pipeline phân tích và tổng hợp dữ liệu sang CSV."""
    logger.info("=== BẮT ĐẦU TỔNG HỢP & PHÂN TÍCH DỮ LIỆU ===")
    try:
        # Đọc dữ liệu sạch từ thư mục config
        cleaned_path = config.CLEANED_CSV_PATH
        df = pd.read_csv(cleaned_path)
        logger.info("Đọc thành công dữ liệu sạch: %d dòng", len(df))

        # Thiết lập đường dẫn đến thư mục 'analytics' lớn nằm trong 'Data dự án'
        output_dir = config.CLEANED_DIR.parent / "analytics"
        
        import os
        os.makedirs(output_dir, exist_ok=True)

        # 2. Thực hiện Thống kê mô tả (Chỉ lưu CSV)
        stats_df = get_descriptive_statistics(df)
        stats_df.to_csv(output_dir / "descriptive_stats.csv", encoding="utf-8-sig")
        print("\n--- BẢNG THỐNG KÊ MÔ TẢ TẠO RA TỪ CODE ---")
        print(stats_df.round(2).to_string())
        print("-" * 42 + "\n")

        # 3. Thực hiện phân tích đơn biến Doanh số, Lợi nhuận, Thời gian (Chỉ lưu CSV)
        uni_financial_time = get_univariate_financial_and_time(df)
        for file_name, uni_df in uni_financial_time.items():
            uni_df.to_csv(output_dir / f"{file_name}.csv", index=False, encoding="utf-8-sig")
        logger.info("Đã xuất các file phân tích đơn biến dạng CSV thành công!")

        # 4. Chạy các hàm phân tích đa biến và chỉ lưu định dạng CSV
        perf_df = get_sales_performance(df)
        perf_df.to_csv(output_dir / "sales_performance.csv", index=False, encoding="utf-8-sig")

        prod_df = get_product_deep_dive(df)
        prod_df.to_csv(output_dir / "product_deep_dive.csv", index=False, encoding="utf-8-sig")

        ship_df = get_shipping_efficiency(df)
        ship_df.to_csv(output_dir / "shipping_efficiency.csv", index=False, encoding="utf-8-sig")

        cohort_df = calculate_cohort_matrix(df)
        cohort_df.to_csv(output_dir / "cohort_retention_matrix.csv", encoding="utf-8-sig")

        logger.info("=== HOÀN TẤT PHÂN TÍCH — Toàn bộ các file CSV đã nằm gọn gàng trong Data dự án/analytics/ ===")

    except FileNotFoundError:
        logger.error("Không tìm thấy file dữ liệu sạch. Vui lòng chạy cleaner.py trước!")
    except Exception as exc:
        logger.exception("Lỗi trong quá trình tổng hợp dữ liệu: %s", exc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_all()