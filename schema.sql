USE retail_db;

CREATE TABLE Countries (
    countryID   VARCHAR(2)  NOT NULL,
    countryName VARCHAR(50) NOT NULL,
    CONSTRAINT pk_countries PRIMARY KEY (countryID)
);

CREATE TABLE Customers(
    customerID char(5) NOT NULL,
    countryID VARCHAR(2) NOT NULL,
    customerName VARCHAR(50) NOT NULL,
    CONSTRAINT PK_customerID PRIMARY KEY(customerID),
    CONSTRAINT FK_countryID FOREIGN KEY(countryID) REFERENCES Countries(countryID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE Invoices(
    invoiceID VARCHAR(7) NOT NULL,
    customerID char(5) NOT NULL,
    invoiceDate DATETIME NOT NULL,
    invoiceStatus VARCHAR(15) NOT NULL DEFAULT 'Completed',
    CONSTRAINT PK_invoiceID PRIMARY KEY(invoiceID),
    CONSTRAINT FK_customerID FOREIGN KEY(customerID) REFERENCES Customers(customerID)
    ON DELETE RESTRICT
    on UPDATE CASCADE,
    CONSTRAINT CK_invoiceStatus CHECK(invoiceStatus IN('Cancelled','Completed')) 
);

CREATE TABLE Products(
    stockCode VARCHAR(10) NOT NULL,
    description VARCHAR(100) NOT NULL,
    unitPrice DECIMAL(10,2) NOT NULL,
    stockQuantity INT NOT NULL DEFAULT 0,
    CONSTRAINT PK_stockCode PRIMARY KEY(stockCode),
    CONSTRAINT CK_unitPrice CHECK(unitPrice >=0)
);

CREATE TABLE InvoiceLine(
    invoiceLineID INT AUTO_INCREMENT,
    invoiceID VARCHAR(7) NOT NULL,
    stockCode VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    CONSTRAINT PK_invoiceLineID PRIMARY KEY(invoiceLineID),
    CONSTRAINT FK_invoiceID FOREIGN KEY(invoiceID) REFERENCES Invoices(invoiceID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT FK_stockCode FOREIGN KEY(stockCode) REFERENCES Products(stockCode)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

