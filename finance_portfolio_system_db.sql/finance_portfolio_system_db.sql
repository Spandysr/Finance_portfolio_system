-- Create database
CREATE DATABASE IF NOT EXISTS finance_portfolio_db;
USE finance_portfolio_db;

-- Investor Table
CREATE TABLE Investor (
    InvestorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE
);

-- Asset Table
CREATE TABLE Asset (
    AssetID INT AUTO_INCREMENT PRIMARY KEY,
    AssetType VARCHAR(50),
    Name VARCHAR(100)
);

-- Portfolio Table
CREATE TABLE Portfolio (
    PortfolioID INT AUTO_INCREMENT PRIMARY KEY,
    InvestorID INT,
    CreatedDate DATE,
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID)
);

-- Investment Table
CREATE TABLE Investment (
    InvestmentID INT AUTO_INCREMENT PRIMARY KEY,
    PortfolioID INT,
    AssetID INT,
    AmountInvested DECIMAL(10, 2),
    DateOfInvestment DATE,
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID),
    FOREIGN KEY (AssetID) REFERENCES Asset(AssetID)
);

-- Transaction Table
CREATE TABLE Transaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    InvestmentID INT,
    TransactionType ENUM('Buy', 'Sell'),
    TransactionDate DATE,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (InvestmentID) REFERENCES Investment(InvestmentID)
);

