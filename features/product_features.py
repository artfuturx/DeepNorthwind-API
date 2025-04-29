import pandas as pd
from data.database_connect import get_db_engine

def get_product_purchase_potential_features():
    engine = get_db_engine()
    query = """
    SELECT
        c."CustomerID",
        p."ProductID",
        p."ProductName",
        p."CategoryID",
        cat."CategoryName",
        SUM(od."UnitPrice" * od."Quantity") AS total_spent_on_category,
        COUNT(DISTINCT o."OrderID") AS order_count_in_category,
        AVG(od."UnitPrice") AS avg_price_in_category
    FROM "Customers" c
    JOIN "Orders" o ON c."CustomerID" = o."CustomerID"
    JOIN "Order Details" od ON o."OrderID" = od."OrderID"
    JOIN "Products" p ON od."ProductID" = p."ProductID"
    JOIN "Categories" cat ON p."CategoryID" = cat."CategoryID"
    GROUP BY c."CustomerID", p."ProductID", p."ProductName", p."CategoryID", cat."CategoryName"
    """
    df = pd.read_sql(query, engine)
    return df