import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

pd.read_sql("SELECT * FROM sqlite_master", conn)

df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
""", conn)


# STEP 2
df_zero_emp = pd.read_sql("""
SELECT o.officeCode,
       o.city
FROM offices o
LEFT JOIN employees e
    ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL;
""", conn)


# STEP 3
df_employee = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       o.city,
       o.state
FROM employees e
LEFT JOIN offices o
    ON e.officeCode = o.officeCode
ORDER BY e.firstName ASC,
         e.lastName ASC;
""", conn)



# STEP 4
df_contacts = pd.read_sql("""
SELECT c.contactFirstName,
       c.contactLastName,
       c.phone,
       c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o
    ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName ASC;
""", conn)



# STEP 5
df_payment = pd.read_sql("""
SELECT c.contactFirstName,
       c.contactLastName,
       p.amount,
       p.paymentDate
FROM customers c
JOIN payments p
    ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)


# STEP 6
df_credit = pd.read_sql("""
SELECT e.employeeNumber,
       e.firstName,
       e.lastName,
       COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber,
         e.firstName,
         e.lastName
HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
ORDER BY numcustomers DESC;
""", conn)



# STEP 7
df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
    ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC;
""", conn)



# STEP 8
df_total_customers = pd.read_sql("""
SELECT p.productName,
       p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od
    ON p.productCode = od.productCode
JOIN orders o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC;
""", conn)



# STEP 9
df_customers = pd.read_sql("""
SELECT o.officeCode,
       o.city,
       COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e
    ON o.officeCode = e.officeCode
LEFT JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY o.officeCode;
""", conn)


# STEP 10
df_under_20 = pd.read_sql("""
WITH under_20_products AS (
    SELECT od.productCode
    FROM orderdetails od
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)

SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    of.city,
    of.officeCode
FROM employees e
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o
    ON c.customerNumber = o.customerNumber
JOIN orderdetails od
    ON o.orderNumber = od.orderNumber
JOIN offices of
    ON e.officeCode = of.officeCode
WHERE od.productCode IN (
    SELECT productCode
    FROM under_20_products
)
ORDER BY e.lastName ASC,
         e.firstName ASC;
""", conn)
























