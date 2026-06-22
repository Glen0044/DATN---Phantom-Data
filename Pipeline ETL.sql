-- Tạo bảng Staging lưu trữ
CREATE TABLE dbo.StagingSuperstore (
    category NVARCHAR(MAX),
    city NVARCHAR(MAX),
    country NVARCHAR(MAX),
    customer_id NVARCHAR(MAX),
    customer_name NVARCHAR(MAX),
    discount NVARCHAR(MAX),
    market NVARCHAR(MAX),
    order_date NVARCHAR(MAX),
    order_id NVARCHAR(MAX),
    order_priority NVARCHAR(MAX),
    product_id NVARCHAR(MAX),
    product_name NVARCHAR(MAX),
    profit NVARCHAR(MAX),
    quantity NVARCHAR(MAX),
    region NVARCHAR(MAX),
    sales NVARCHAR(MAX),
    segment NVARCHAR(MAX),
    ship_date NVARCHAR(MAX),
    ship_mode NVARCHAR(MAX),
    shipping_cost NVARCHAR(MAX),
    state NVARCHAR(MAX),
    sub_category NVARCHAR(MAX),
    profit_margin NVARCHAR(MAX),
    ship_delay NVARCHAR(MAX),
    order_year NVARCHAR(MAX),
    order_quarter NVARCHAR(MAX),
    order_month NVARCHAR(MAX),
    cohort_month NVARCHAR(MAX),
    cohort_index NVARCHAR(MAX)
);

-- Import data
BULK INSERT dbo.StagingSuperstore
FROM 'D:\DATN\DATN---Phantom-Data\Dataset\data\cleaned\superstore_sql_import.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = '|',
    FIELDQUOTE = '"',
    CODEPAGE = '65001',
    ROWTERMINATOR = '0x0a',
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