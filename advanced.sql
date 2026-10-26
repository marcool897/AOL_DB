USE retail_db;


-- 1. TRIGGER: Update stockQuantity di Products setiap kali ada transaksi


DELIMITER $$

CREATE TRIGGER trg_update_stock_after_invoiceline_insert
AFTER INSERT ON InvoiceLine
FOR EACH ROW
BEGIN
    DECLARE v_invoiceStatus VARCHAR(15);

    SELECT invoiceStatus INTO v_invoiceStatus
    FROM Invoices
    WHERE invoiceID = NEW.invoiceID;

    IF v_invoiceStatus = 'Cancelled' THEN
        UPDATE Products
        SET stockQuantity = stockQuantity + NEW.quantity
        WHERE stockCode = NEW.stockCode;
    ELSE
        UPDATE Products
        SET stockQuantity = stockQuantity - NEW.quantity
        WHERE stockCode = NEW.stockCode;
    END IF;
END$$

DELIMITER ;

-- 2. STORED PROCEDURE: GetCustomerInvoiceHistory
-- Menerima CustomerID, mengembalikan daftar semua invoice milik customer


DELIMITER $$

CREATE PROCEDURE GetCustomerInvoiceHistory(
    IN p_customerID CHAR(5)
)
BEGIN
    SELECT
        i.invoiceID,
        i.invoiceDate,
        i.invoiceStatus,
        SUM(il.quantity * p.unitPrice) AS total_value
    FROM Invoices i
    JOIN InvoiceLine il ON i.invoiceID = il.invoiceID
    JOIN Products p ON il.stockCode = p.stockCode
    WHERE i.customerID = p_customerID
    GROUP BY i.invoiceID, i.invoiceDate, i.invoiceStatus
    ORDER BY i.invoiceDate DESC;
END$$

DELIMITER ;
