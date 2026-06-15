
import logging
import pandas as pd
import numpy as np
import config

logger = logging.getLogger("aggregate")


# 1. Hàm Thống kê mô tả (Descriptive Statistics)
def get_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sử dụng NumPy và Pandas để tính toán các chỉ số tập trung (Mean, Median)
    và chỉ số phân tán (Std, Min, Max, IQR) của các biến định lượng.
    """
    logger.info("Đang tính toán Thống kê mô tả (Descriptive Statistics)...")
    
    numeric_cols = ['sales', 'profit', 'discount', 'shipping_cost', 'ship_delay_days']
    
    # Tính toán các chỉ số cơ bản
    stats = df[numeric_cols].describe().T
    
    # Bổ sung Trung vị (Median) và Biên độ phân tán (Range) bằng NumPy/Pandas
    stats['median'] = df[numeric_cols].median()
    stats['range'] = stats['max'] - stats['min']
    
    # Sắp xếp lại cột cho đẹp mắt
    stats = stats[['count', 'mean', 'median', 'std', 'min', 'max', 'range', '25%', '75%']]
    return stats


# 2. Hàm Phân tích Đa biến: Hiệu suất kinh doanh theo Năm và Thị trường
def get_sales_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích mối quan hệ giữa Năm đặt hàng, Thị trường đối với Doanh số và Lợi nhuận.
    """
    logger.info("Phân tích đa biến: Tổng hợp hiệu suất kinh doanh theo Năm và Thị trường...")
    
    perf = df.groupby(['order_year', 'market']).agg(
        total_sales    = ('sales', 'sum'),
        total_profit   = ('profit', 'sum'),
        total_quantity = ('quantity', 'sum'),
        avg_discount   = ('discount', 'mean')
    ).reset_index()
    
    # Tính biên lợi nhuận sau khi group
    perf['profit_margin'] = perf['total_profit'] / perf['total_sales']
    return perf


# 3. Hàm Phân tích Đa biến: Chi tiết Ngành hàng (Category & Sub-Category)
def get_product_deep_dive(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích sâu hiệu suất tài chính theo Danh mục chính và Danh mục con để phát hiện hàng gánh lỗ.
    """
    logger.info("Phân tích đa biến: Bóc tách hiệu suất theo Ngành hàng (Category & Sub-Category)...")
    
    product_analysis = df.groupby(['category', 'sub_category']).agg(
        total_sales    = ('sales', 'sum'),
        total_profit   = ('profit', 'sum'),
        avg_discount   = ('discount', 'mean'),
        order_count    = ('order_id', 'nunique')
    ).reset_index()
    
    product_analysis['profit_margin'] = product_analysis['total_profit'] / product_analysis['total_sales']
    # Sắp xếp theo lợi nhuận giảm dần
    product_analysis = product_analysis.sort_values(by='total_profit', ascending=False)
    return product_analysis


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
    
    # Nhóm theo Cohort Month và Cohort Index để đếm số lượng khách hàng duy nhất mua lại
    cohort_group = df.groupby(['cohort_month', 'cohort_index']).agg(
        unique_customers = ('customer_id', 'nunique')
    ).reset_index()
    
    # Biến đổi bảng thành dạng Ma trận xoay (Pivot Table)
    cohort_matrix = cohort_group.pivot(
        index='cohort_month', 
        columns='cohort_index', 
        values='unique_customers'
    )
    
    # Tính toán tỷ lệ phần trăm giữ chân (Retention Rate)
    cohort_size = cohort_matrix.iloc[:, 0]  # Lấy số lượng khách hàng tháng đầu tiên làm gốc
    cohort_retention = cohort_matrix.divide(cohort_size, axis=0)  # Chia tỷ lệ cho toàn ma trận
    
    return cohort_retention


# ──────────────────────────────────────────────────────────────
def get_univariate_financial_and_time(df: pd.DataFrame) -> dict:
    """
    Phân tích đơn biến chuyên sâu cho Doanh số, Lợi nhuận và Thời gian.
    """
    logger.info("Đang thực hiện phân tích đơn biến cho Sales, Profit và Time...")
    uni_results = {}
    
    # ------------------------------------------------------------------
    # A. PHÂN TÍCH ĐƠN BIẾN: DOANH SỐ (Sales Binning)
    # Khảo sát phân phối các mức giá trị của đơn hàng
    sales_bins = [0, 10, 50, 100, 500, 1000, 5000, np.inf]
    sales_labels = ['Under $10', '$10-$50', '$50-$100', '$100-$500', '$500-$1000', '$1000-$5000', 'Over $5000']
    
    df['sales_group'] = pd.cut(df['sales'], bins=sales_bins, labels=sales_labels)
    sales_counts = df['sales_group'].value_counts()
    sales_pct = df['sales_group'].value_counts(normalize=True) * 100
    
    uni_results['uni_sales_distribution'] = pd.DataFrame({
        'sales_range': sales_counts.index,
        'order_count': sales_counts.values,
        'percentage_or': sales_pct.values
    }).sort_values(by='sales_range') # Sắp xếp theo thứ tự khoảng giá

    # ------------------------------------------------------------------
    # B. PHÂN TÍCH ĐƠN BIẾN: LỢI NHUẬN (Profit Status)
    # Khảo sát xem cơ cấu có bao nhiêu đơn hàng có lãi, hòa vốn, và lỗ
    df['profit_status'] = np.select(
        condlist=[df['profit'] > 0, df['profit'] == 0, df['profit'] < 0],
        choicelist=['Profitable (Lãi)', 'Breakeven (Hòa vốn)', 'Loss-making (Lỗ)'],
        default='Unknown'
    )
    profit_counts = df['profit_status'].value_counts()
    profit_pct = df['profit_status'].value_counts(normalize=True) * 100
    
    uni_results['uni_profit_status'] = pd.DataFrame({
        'profit_status': profit_counts.index,
        'order_count': profit_counts.values,
        'percentage_or': profit_pct.values
    })

    # ------------------------------------------------------------------
    # C. PHÂN TÍCH ĐƠN BIẾN: THỜI GIAN (Order Seasonality)
    # Trích xuất tháng độc lập (từ tháng 1 đến tháng 12) để tìm quy luật mùa vụ không phụ thuộc vào năm
    df['order_month_only'] = pd.to_datetime(df['order_date']).dt.month
    
    time_counts = df['order_month_only'].value_counts()
    time_pct = df['order_month_only'].value_counts(normalize=True) * 100
    
    uni_results['uni_time_seasonality'] = pd.DataFrame({
        'month': time_counts.index,
        'order_count': time_counts.values,
        'percentage_or': time_pct.values
    }).sort_values(by='month') # Sắp xếp từ tháng 1 đến tháng 12

    return uni_results

def run_all() -> None:
    """Chạy toàn bộ pipeline phân tích và tổng hợp dữ liệu."""
    logger.info("=== BẮT ĐẦU TỔNG HỢP & PHÂN TÍCH DỮ LIỆU ===")
    try:
        # 1. Đọc dữ liệu sạch từ data/cleaned/
        cleaned_path = config.CLEANED_DIR / "superstore_cleaned.csv"
        df = pd.read_csv(cleaned_path)
        logger.info("Đọc thành công dữ liệu sạch: %d dòng", len(df))

        # Tự động tạo thư mục chứa kết quả phân tích nếu chưa có
        output_dir = config.BASE_DIR / "data" / "analytics"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 2. Thực hiện Thống kê mô tả
        stats_df = get_descriptive_statistics(df)
        stats_df.to_csv(output_dir / "descriptive_stats.csv", encoding="utf-8-sig")

        # 3. MỚI: Thực hiện phân tích đơn biến Doanh số, Lợi nhuận, Thời gian
        uni_financial_time = get_univariate_financial_and_time(df)
        for file_name, uni_df in uni_financial_time.items():
            uni_df.to_csv(output_dir / f"{file_name}.csv", index=False, encoding="utf-8-sig")
        logger.info("Đã xuất các file phân tích đơn biến tài chính và thời gian thành công!")

        # 4. Chạy các hàm phân tích đa biến khác (Giữ nguyên phần cũ của bạn)
        perf_df = get_sales_performance(df)
        perf_df.to_csv(output_dir / "sales_performance.csv", index=False, encoding="utf-8-sig")

        prod_df = get_product_deep_dive(df)
        prod_df.to_csv(output_dir / "product_deep_dive.csv", index=False, encoding="utf-8-sig")

        ship_df = get_shipping_efficiency(df)
        ship_df.to_csv(output_dir / "shipping_efficiency.csv", index=False, encoding="utf-8-sig")

        cohort_df = calculate_cohort_matrix(df)
        cohort_df.to_csv(output_dir / "cohort_retention_matrix.csv", encoding="utf-8-sig")

        logger.info("=== HOÀN TẤT PHÂN TÍCH — Các file đã được lưu tại data/analytics/ ===")

    except FileNotFoundError:
        logger.error("Không tìm thấy file dữ liệu sạch. Vui lòng chạy cleaner.py trước!")
    except Exception as exc:
        logger.exception("Lỗi trong quá trình tổng hợp dữ liệu: %s", exc)
        
if __name__ == "__main__":
    # Cấu hình log cơ bản để chạy độc lập
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_all()