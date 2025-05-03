"""
Dosya Adı: features/customer_features.py
Amaç: Müşteri verilerinden özellik çıkarımı yaparak, müşteri yeniden sipariş tahmin modeli için gerekli özellikleri hazırlar.
Yapılanlar: Müşteri sipariş geçmişi, sipariş sıklığı, ortalama sipariş tutarı gibi sayısal özellikler çıkarılır.
Hedef Değişken: Müşterinin son siparişinden sonraki 6 ay içinde tekrar sipariş verip vermediği (1: evet, 0: hayır).
API Endpoint: Bu veri, müşteri yeniden sipariş tahmin modelini eğitmek için kullanılacak ve API endpoint'te tahmin yapmak için kullanılacak.
"""

import pandas as pd
from data.database_connect import engine

def get_customer_order_features():
    """
    Müşteri sipariş özelliklerini hesaplar:
    - Toplam harcama
    - Sipariş sayısı
    - Ortalama sipariş büyüklüğü
    - Son sipariş tarihi
    """
    query = """
    SELECT 
        c.customer_id,
        c.company_name,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(od.unit_price * od.quantity * (1 - od.discount)) as total_spent,
        AVG(od.unit_price * od.quantity * (1 - od.discount)) as avg_order_value,
        MAX(o.order_date) as last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_details od ON o.order_id = od.order_id
    GROUP BY c.customer_id, c.company_name
    """
    df = pd.read_sql(query, engine)
    df['last_order_date'] = pd.to_datetime(df['last_order_date'])
    return df

def add_target_variable(df):
    """
    Hedef değişkeni ekler: Müşterinin son siparişinden sonraki 6 ay içinde tekrar sipariş verip vermediği
    """
    # Son siparişten 6 ay sonrasını hesapla
    df['six_months_after'] = df['last_order_date'] + pd.DateOffset(months=6)
    
    # Müşterilerin tüm siparişlerini al
    orders_query = """
    SELECT customer_id, order_date 
    FROM orders
    """
    orders = pd.read_sql(orders_query, engine)
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # Müşteri bazında tekrar sipariş kontrolü
    df['repeat_purchase_within_6m'] = 0
    
    for idx, row in df.iterrows():
        customer_orders = orders[orders['customer_id'] == row['customer_id']]
        repeat_orders = customer_orders[
            (customer_orders['order_date'] > row['last_order_date']) & 
            (customer_orders['order_date'] <= row['six_months_after'])
        ]
        df.at[idx, 'repeat_purchase_within_6m'] = 1 if len(repeat_orders) > 0 else 0
    
    return df

# Test için
if __name__ == "__main__":
    # Özellikleri al
    df = get_customer_order_features()
    print("\nMüşteri Özellikleri:")
    print(df.head())
    
    # Hedef değişkeni ekle
    df = add_target_variable(df)
    print("\nHedef Değişken Eklendi:")
    print(df.head())
