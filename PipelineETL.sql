-- Tạo bảng Staging lưu trữ
CREATE TABLE dbo.StagingSuperstore
(
    category NVARCHAR(50),
    city NVARCHAR(100),
    country NVARCHAR(100),
    customer_id NVARCHAR(50),
    customer_name NVARCHAR(150),
    discount NVARCHAR(50),
    market NVARCHAR(50),
    order_date NVARCHAR(50),
    order_id NVARCHAR(50),
    order_priority NVARCHAR(50),
    product_id NVARCHAR(50),
    product_name NVARCHAR(500),
    profit NVARCHAR(50),
    quantity NVARCHAR(50),
    region NVARCHAR(100),
    sales NVARCHAR(50),
    segment NVARCHAR(50),
    ship_date NVARCHAR(50),
    ship_mode NVARCHAR(50),
    shipping_cost NVARCHAR(50),
    state NVARCHAR(100),
    sub_category NVARCHAR(100),
    discount_pct NVARCHAR(50),
    profit_margin NVARCHAR(100),
    ship_delay_days NVARCHAR(50),
    order_year NVARCHAR(50),
    order_quarter NVARCHAR(50),
    order_month NVARCHAR(50),
    cohort_month NVARCHAR(50),
    cohort_index NVARCHAR(50)
);

BULK INSERT dbo.StagingSuperstore
FROM 'D:\DATN\DATN---Phantom-Data\Data dự án\cleaned\superstore_cleaned.csv'
WITH
(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    CODEPAGE = '65001',
    TABLOCK
);

-- Đếm số dòng:
SELECT COUNT(*)
FROM StagingSuperstore;

-- Kiểm tra null: 
SELECT *
FROM StagingSuperstore
WHERE customer_id IS NULL;

-- Kiểm tra dữ liệu trùng:
SELECT order_id,
COUNT(*)
FROM StagingSuperstore
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Load dữ liệu bảng DimCustomer
INSERT INTO DimCustomer
(
CustomerID,
CustomerName,
Segment
)
SELECT DISTINCT
customer_id,
customer_name,
Segment
FROM StagingSuperstore;

-- Load dữ liệu vào bảng DimProduct
INSERT INTO dbo.DimProduct
(
    ProductID,
    ProductName,
    Category,
    SubCategory
)
SELECT
    product_id,
    MAX(product_name) AS ProductName,
    MAX(category) AS Category,
    MAX(sub_category) AS SubCategory
FROM dbo.StagingSuperstore
WHERE product_id NOT IN (
    SELECT ProductID FROM dbo.DimProduct
)
GROUP BY product_id;

-- Load dữ liệu vào bảng DimLocation
INSERT INTO DimLocation
(
Country,
Region,
State,
City
)
SELECT DISTINCT
Country,
Region,
State,
City
FROM StagingSuperstore;

-- Load dữ liệu vào bảng DimShipMode
INSERT INTO DimShipMode
(
ShipMode
)
SELECT DISTINCT
ship_mode
FROM StagingSuperstore;

-- Tạo DimDate
INSERT INTO DimDate
(
DateKey,
FullDate,
Year,
QuarterNo,
MonthNo,
MonthName
)
SELECT DISTINCT
YEAR(order_date)*10000 + MONTH(order_date)*100 + DAY(order_date),
order_date,
YEAR(order_date),
DATEPART(QUARTER,order_date),
MONTH(order_date),
DATENAME(MONTH,order_date)
FROM StagingSuperstore;

-- load bảng chính là Fact Table
INSERT INTO FactSales
(
OrderID,
CustomerKey,
ProductKey,
LocationKey,
ShipModeKey,
DateKey,
Sales,
Quantity,
Discount,
Profit
)
SELECT
s.order_id,
c.CustomerKey,
p.ProductKey,
l.LocationKey,
sm.ShipModeKey,
YEAR(s.order_date)*10000 + MONTH(s.order_date)*100 + DAY(s.order_date),
s.Sales,
s.Quantity,
s.Discount,
s.Profit
FROM StagingSuperstore s
JOIN DimCustomer c
ON s.customer_id = c.CustomerID
JOIN DimProduct p
ON s.product_id = p.ProductID
JOIN DimLocation l
ON s.City = l.City
AND s.Country = l.Country
JOIN DimShipMode sm
ON s.ship_mode = sm.ShipMode;