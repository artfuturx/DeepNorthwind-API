import pandas as pd
from data.database_connect import get_db_engine  # Kendi bağlantı fonksiyonunu import et!

def get_customer_order_features():
    engine = get_db_engine()
    query = """
    SELECT
        c."CustomerID",
        c."CompanyName",
        COUNT(o."OrderID") as total_orders,
        SUM(od."UnitPrice" * od."Quantity") as total_spent,
        AVG(od."UnitPrice" * od."Quantity") as avg_order_value,
        MAX(o."OrderDate") as last_order_date
    FROM "Customers" c
    LEFT JOIN "Orders" o ON c."CustomerID" = o."CustomerID"
    LEFT JOIN "Order Details" od ON o."OrderID" = od."OrderID"
    GROUP BY c."CustomerID", c."CompanyName"
    """
    df = pd.read_sql(query, engine)
    return df