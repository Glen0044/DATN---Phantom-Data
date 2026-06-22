PHÂN TÍCH HIỆU QUẢ KINH DOANH CHUỖI BÁN LẺ SUPERSTORE
1. Giới thiệu dự án

Dự án được thực hiện nhằm phân tích hiệu quả kinh doanh của chuỗi bán lẻ Superstore thông qua việc xây dựng quy trình xử lý dữ liệu hoàn chỉnh từ thu thập, lưu trữ, làm sạch, biến đổi đến khám phá dữ liệu.

Mục tiêu của dự án là hỗ trợ doanh nghiệp đánh giá tình hình kinh doanh, hiệu quả sản phẩm, khách hàng và khu vực bán hàng, từ đó đưa ra các quyết định dựa trên dữ liệu (Data-Driven Decision Making).

2. Bài toán nghiệp vụ

Doanh nghiệp cần trả lời các câu hỏi:

Doanh thu và lợi nhuận đang phân bố như thế nào?
Nhóm sản phẩm nào mang lại hiệu quả kinh doanh cao nhất?
Khu vực nào đóng góp doanh thu lớn nhất?
Khách hàng nào mang lại nhiều giá trị cho doanh nghiệp?
Mức chiết khấu có ảnh hưởng như thế nào đến lợi nhuận?
Có những xu hướng hoặc quy luật nào ẩn trong dữ liệu bán hàng?
3. Nguồn dữ liệu
    Dataset sử dụng

    - Superstore Dataset

    Thông tin dữ liệu

    Bộ dữ liệu chứa thông tin về:

    | STT | Tên trường    | Mô tả                                                   |
    | --- | ------------- | ------------------------------------------------------- |
    | 1   | Order ID      | Mã đơn hàng                                             |
    | 2   | Order Date    | Ngày đặt hàng                                           |
    | 3   | Ship Date     | Ngày giao hàng                                          |
    | 4   | Customer ID   | Mã khách hàng                                           |
    | 5   | Customer Name | Tên khách hàng                                          |
    | 6   | Segment       | Phân khúc khách hàng (Consumer, Corporate, Home Office) |
    | 7   | Country       | Quốc gia                                                |
    | 8   | State         | Bang/Tỉnh                                               |
    | 9   | City          | Thành phố                                               |
    | 10  | Region        | Khu vực kinh doanh                                      |
    | 11  | Product ID    | Mã sản phẩm                                             |
    | 12  | Product Name  | Tên sản phẩm                                            |
    | 13  | Category      | Danh mục sản phẩm                                       |
    | 14  | Sub-Category  | Danh mục con                                            |
    | 15  | Sales         | Doanh thu bán hàng                                      |
    | 16  | Quantity      | Số lượng sản phẩm bán ra                                |
    | 17  | Discount      | Mức chiết khấu áp dụng                                  |
    | 18  | Profit        | Lợi nhuận thu được                                      |
    | 19  | Shipping Cost | Chi phí vận chuyển                                      |
    | 20  | Ship Mode     | Phương thức giao hàng                                   |

    Phương pháp thu thập dữ liệu

    Dữ liệu được thu thập từ bộ dữ liệu mẫu Superstore dưới định dạng CSV và được đưa vào hệ thống để xử lý thông qua Python và SQL Server.

4. Data Warehouse và ETL
    Kiến trúc dữ liệu

    Dự án sử dụng mô hình Star Schema gồm:

    Fact Table

    FactSales

    Dimension Tables
    DimCustomer
    DimProduct
    DimLocation
    DimDate
    Quy trình ETL
    Đọc dữ liệu từ file CSV.
    Đưa dữ liệu vào Staging Area.
    Làm sạch và chuẩn hóa dữ liệu bằng Python.
    Nạp dữ liệu vào Data Warehouse.
    Tạo các bảng Fact và Dimension phục vụ phân tích.
5. Làm sạch dữ liệu (Data Cleaning)

    Các bước làm sạch dữ liệu bao gồm:

    Xử lý dữ liệu thiếu
    Điền giá trị mặc định cho Postal Code.
    Chuyển các giá trị số về đúng kiểu dữ liệu.
    Thay thế giá trị Null bằng 0 đối với các trường số.
    Xử lý dữ liệu trùng lặp
    Loại bỏ các bản ghi trùng lặp dựa trên Order ID và Product ID.
    Xử lý lỗi nghiệp vụ
    Loại bỏ các đơn hàng có ngày giao hàng nhỏ hơn ngày đặt hàng.
    Chuẩn hóa dữ liệu
    Chuẩn hóa tên cột.
    Chuẩn hóa định dạng ngày tháng.
    Chuẩn hóa kiểu dữ liệu số và văn bản.
6. Biến đổi dữ liệu (Data Transformation)

    Nhóm xây dựng thêm các thuộc tính phục vụ phân tích:

   
7. Khám phá dữ liệu (EDA)
    Phân tích doanh thu
    Doanh thu theo thời gian.
    Doanh thu theo khu vực.
    Doanh thu theo danh mục sản phẩm.
    Phân tích lợi nhuận
    Sản phẩm có lợi nhuận cao nhất.
    Sản phẩm có lợi nhuận thấp hoặc âm.
    Tác động của chiết khấu đến lợi nhuận.
    Phân tích khách hàng
    Phân khúc khách hàng theo RFM.
    Khách hàng mang lại doanh thu cao.
    Tần suất mua hàng của khách hàng.
    Phân tích vận chuyển
    Thời gian giao hàng trung bình.
    So sánh hiệu quả giữa các phương thức giao hàng.
8. Công nghệ sử dụng
    SQL Server
    Thiết kế Data Warehouse
    Lưu trữ dữ liệu
    Quản lý Fact và Dimension Tables
    Python
    ETL Pipeline
    Data Cleaning
    Feature Engineering
    Tableau
    Kết nối Data Warehouse
    Xây dựng Dashboard
    Trực quan hóa dữ liệu