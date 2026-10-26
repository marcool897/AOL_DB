-- Query 1:

UPDATE Products
SET unitPrice = unitPrice * 1.08
WHERE unitPrice < 5.00;

-- Query 2: 
UPDATE Invoices
SET InvoiceStatus = 'Cancelled'
WHERE invoiceID LIKE 'C%';

-- Query 3:
SELECT
    co.countryName,
    SUM(il.quantity * p.unitPrice) AS total_revenue,
    COUNT(DISTINCT i.invoiceID) AS total_completed_invoices
FROM Invoices i
JOIN Customers cu ON i.customerID = cu.customerID
JOIN Countries co ON cu.countryID = co.countryID
JOIN InvoiceLine il ON i.invoiceID = il.invoiceID
JOIN Products p ON il.stockCode = p.stockCode
WHERE i.invoiceStatus = 'Completed'
GROUP BY co.countryName
ORDER BY total_revenue DESC;

-- Query 4:

SELECT
    cu.customerID,
    cu.customerName,
    customer_spend.total_spend
FROM Customers cu
JOIN (
    SELECT
        i.customerID,
        SUM(il.quantity * p.unitPrice) AS total_spend
    FROM Invoices i
    JOIN InvoiceLine il ON i.invoiceID = il.invoiceID
    JOIN Products p ON il.stockCode = p.stockCode
    GROUP BY i.customerID
) AS customer_spend ON cu.customerID = customer_spend.customerID
WHERE customer_spend.total_spend > (
    SELECT AVG(total_spend)
    FROM (
        SELECT
            i.customerID,
            SUM(il.quantity * p.unitPrice) AS total_spend
        FROM Invoices i
        JOIN InvoiceLine il ON i.invoiceID = il.invoiceID
        JOIN Products p ON il.stockCode = p.stockCode
        GROUP BY i.customerID
    ) AS all_customer_spend
)
ORDER BY customer_spend.total_spend DESC;

-- Query 5:

SELECT
    p.stockCode,
    p.description,
    COUNT(DISTINCT co.countryName) AS jumlah_negara_pembeli
FROM Products p
JOIN InvoiceLine il ON p.stockCode = il.stockCode
JOIN Invoices i ON il.invoiceID = i.invoiceID
JOIN Customers cu ON i.customerID = cu.customerID
JOIN Countries co ON cu.countryID = co.countryID
WHERE p.stockCode NOT IN (
    SELECT il2.stockCode
    FROM InvoiceLine il2
    JOIN Invoices i2 ON il2.invoiceID = i2.invoiceID
    JOIN Customers cu2 ON i2.customerID = cu2.customerID
    JOIN Countries co2 ON cu2.countryID = co2.countryID
    WHERE co2.countryName = 'Germany'
)
GROUP BY p.stockCode, p.description
HAVING COUNT(DISTINCT co.countryName) >= 2;