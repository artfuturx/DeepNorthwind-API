"""
Dosya Adı: features/product_features.py
Amaç: Ürün verilerinden özellik çıkarımı yaparak, ürün satın alma potansiyeli tahmin modeli için gerekli özellikleri hazırlar.
Yapılanlar: Ürün satış geçmişi, stok durumu, fiyat bilgisi gibi sayısal özellikler çıkarılır.
Hedef Değişken: Ürünün satın alma potansiyeli (1: yüksek, 0: düşük).
API Endpoint: Bu veri, ürün satın alma potansiyeli tahmin modelini eğitmek için kullanılacak ve API endpoint'te tahmin yapmak için kullanılacak.
API Kullanımı: API endpoint'ine müşteri ID ve ürün detayları gönderilerek, ürünün satın alma potansiyeli tahmin edilir.
"""
import pandas as pd
import numpy as np
from data.database_connect import engine
from features.customer_features import get_customer_order_features

def prepare_category_features():
    """
    Kategori bazlı özellikleri hazırlar
    """
    query = """
    SELECT
        c.customer_id,
        cat.category_name,
        SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_spent_in_category,
        COUNT(DISTINCT o.order_id) AS order_count_in_category
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
    GROUP BY c.customer_id, cat.category_name
    """
    df = pd.read_sql(query, engine)
    # Kategori bazında pivot table oluştur
    pivot_features = df.pivot_table(
        index='customer_id',
        columns='category_name',
        values=['total_spent_in_category', 'order_count_in_category'],
        fill_value=0
    )
    # Sütun isimlerini düzenle
    pivot_features.columns = [f"{col[0]}_{col[1]}" for col in pivot_features.columns]
    # Toplam harcama ve sipariş sayısını hesapla
    total_features = df.groupby('customer_id').agg({
        'total_spent_in_category': 'sum',
        'order_count_in_category': 'sum'
    }).rename(columns={
        'total_spent_in_category': 'total_spent',
        'order_count_in_category': 'total_orders'
    })
    # Özellikleri birleştir
    return pd.concat([pivot_features, total_features], axis=1)

def get_new_product_features(product_id):
    """
    Yeni ürünün özelliklerini getirir
    """
    query = """
    SELECT
        p.product_id,
        p.product_name,
        p.unit_price,
        cat.category_name
    FROM products p
    JOIN categories cat ON p.category_id = cat.category_id
    WHERE p.product_id = %s
    """
    df = pd.read_sql(query, engine, params=[product_id])
    return df

def add_purchase_potential_label(df):
    """
    Satın alma potansiyeli etiketini ekler
    """
    # Son 3 ayda satın alma yapmış müşterileri etiketle
    current_date = pd.Timestamp.now()
    three_months_ago = current_date - pd.DateOffset(months=3)
    df['recent_purchase'] = (pd.to_datetime(df['last_order_date']) >= three_months_ago).astype(int)
    return df

def get_customer_category_features():
    """
    Müşterilerin her kategoriye yaptığı toplam harcamayı hesaplar.
    """
    query = """
    SELECT 
        c.customer_id,
        cat.category_name,
        SUM(od.unit_price * od.quantity * (1 - od.discount)) as total_spent_in_category,
        COUNT(DISTINCT o.order_id) as total_orders_in_category
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
    GROUP BY c.customer_id, cat.category_name
    """
    df = pd.read_sql(query, engine)
    return df

def pivot_customer_category_features(df):
    """
    Her müşteri için kategori bazlı harcamaları pivot tabloya çevirir.
    """
    pivot = df.pivot_table(index='customer_id', 
                          columns='category_name', 
                          values='total_spent_in_category', 
                          fill_value=0)
    pivot.columns = [f'spent_{col.lower()}' for col in pivot.columns]
    pivot.reset_index(inplace=True)
    return pivot

def prepare_purchase_potential_features():
    """
    Model için kullanılacak müşteri-kategori harcama veri setini hazırlar.
    """
    df = get_customer_category_features()
    pivot = pivot_customer_category_features(df)
    return pivot

def prepare_purchase_potential_data():
    """
    Satın alma potansiyeli tahmini için veriyi hazırlar
    """
    # Müşteri özelliklerini al
    customer_df = get_customer_order_features()
    # Kategori özelliklerini al
    category_df = prepare_category_features()
    # Verileri birleştir
    df = pd.merge(customer_df, category_df, on='customer_id', how='inner')
    # Hedef değişkeni ekle
    df = add_purchase_potential_label(df)
    return df

if __name__ == "__main__":
    # Test için örnek kullanım
    df = prepare_purchase_potential_data()
    print("\nSatın Alma Potansiyeli Veri Seti:")
    print(df.head())
    print("\nÖzellikler:", df.columns.tolist())
    features = prepare_purchase_potential_features()
    print("\nMüşteri-Kategori Harcama Özellikleri:")
    print(features.head())

"""

    ## 3. Yeni Ürün Satın Alma Potansiyeli Modeli

### Veri Hazırlama

- Products, Categories, Order Details ve Orders tablolarını birleştir
- Kategori bazında harcama
- Fiyat duyarlılığı
- Kategori bazında satın alma sıklığı

### Model Geliştirme

- Kategorileri one-hot encode etme
- Müşteri gömme (embedding) vektörleri oluşturma
- Kategori yakınlık skorları hesaplama
- Sinir ağı modeli inşa etme

### Ar-Ge Konuları

- Öneri Sistemleri: Neural Collaborative Filtering
- Otomatik Kodlayıcılar (AutoEncoders)
- Çoklu Etiket Tahmini: Birden fazla ürün önerisi için çıktı katmanı modifikasyonu

### API Uygulaması

- Endpoint: `/purchase_potential`
- Girdi: Müşteri ID ve yeni ürün detayları
- Çıktı: Satın alma olasılığı ve benzer önerilen ürünler"""