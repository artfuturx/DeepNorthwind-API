from sqlalchemy import create_engine
import pandas as pd

def load_and_print_tables(table_names, engine):
    """
    Verilen tabloları veritabanından okur ve ekrana yazdırır.
    """
    for table in table_names:
        query = f'SELECT * FROM "{table}";'
        df = pd.read_sql(query, engine)
        print(f"\n--- {table} ---")
        print(df.head())

def get_engine():
    """
    Veritabanı bağlantısını döndürür.
    """
    return create_engine("postgresql+psycopg2://sevgi:140216@localhost:5432/northwind")

# Kullanım
if __name__ == "__main__":
    engine = get_engine()
    tables = ["Customers", "Orders", "Order Details", "Products"]
    load_and_print_tables(tables, engine)