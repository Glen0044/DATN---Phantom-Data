CREATE DATABASE DataWarehouse;
GO

USE DataWarehouse;

--Bảng DimCustomer

CREATE TABLE DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID NVARCHAR(50) UNIQUE,
    CustomerName NVARCHAR(255),
    Segment NVARCHAR(100)
);
-- bảng DimProduct

CREATE TABLE DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,
    ProductID NVARCHAR(50) UNIQUE,
    ProductName NVARCHAR(255),
    Category NVARCHAR(100),
    SubCategory NVARCHAR(100)
);
--bảng DimLocation

CREATE TABLE DimLocation (
    LocationKey INT IDENTITY(1,1) PRIMARY KEY,
    Country NVARCHAR(100),
    Region NVARCHAR(100),
    State NVARCHAR(100),
    City NVARCHAR(100)
);
--bảng DimShipMode

CREATE TABLE DimShipMode (
    ShipModeKey INT IDENTITY(1,1) PRIMARY KEY,
    ShipMode NVARCHAR(100) UNIQUE
);
--bảng DimDate

CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    FullDate DATE,
    [Year] INT,
    QuarterNo INT,
    MonthNo INT,
    MonthName NVARCHAR(20)
);
--bảng chính Fact Table

CREATE TABLE FactSales (

    SalesKey INT IDENTITY(1,1) PRIMARY KEY,

    OrderID NVARCHAR(50),

    CustomerKey INT,
    ProductKey INT,
    LocationKey INT,
    ShipModeKey INT,
    DateKey INT,

    Sales DECIMAL(18,2),
    Quantity INT,
    Discount DECIMAL(18,2),
    Profit DECIMAL(18,2),

    FOREIGN KEY (CustomerKey)
        REFERENCES DimCustomer(CustomerKey),

    FOREIGN KEY (ProductKey)
        REFERENCES DimProduct(ProductKey),

    FOREIGN KEY (LocationKey)
        REFERENCES DimLocation(LocationKey),

    FOREIGN KEY (ShipModeKey)
        REFERENCES DimShipMode(ShipModeKey),

    FOREIGN KEY (DateKey)
        REFERENCES DimDate(DateKey)
);