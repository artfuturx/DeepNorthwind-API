from sqlalchemy import create_engine
import pandas as pd

# Veritabanı bağlantısı 
engine = create_engine("postgresql+psycopg://sevgi:140216@localhost:5432/northwind")

tables = ["customers", "orders", "products"]
for table in tables:
    print(f"\n--- {table} Tablosu ---")
    df = pd.read_sql(f'SELECT * FROM "{table}" LIMIT 5', engine)
    print(df)