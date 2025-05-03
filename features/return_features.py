"""
Dosya Adı: features/return_features.py
Amaç: İade verilerinden özellik çıkarımı yaparak, iade riski tahmin modeli için gerekli özellikleri hazırlar.
Yapılanlar: İade geçmişi, sipariş detayları, müşteri bilgileri gibi sayısal özellikler çıkarılır.
Hedef Değişken: İade riski (1: yüksek, 0: düşük).
API Endpoint: Bu veri, iade riski tahmin modelini eğitmek için kullanılacak ve API endpoint'te tahmin yapmak için kullanılacak.
"""
import pandas as pd
from data.database_connect import engine

def get_order_features():
    """
    Sipariş bazında temel özellikleri hesaplar:
    - quantity, unit_price, discount, total_amount, discount_percent
    """
    query = """
    SELECT 
        od.order_id,
        od.product_id,
        p.product_name,
        od.quantity,
        od.unit_price,
        od.discount,
        (od.unit_price * od.quantity * (1 - od.discount)) as total_amount
    FROM order_details od
    JOIN products p ON od.product_id = p.product_id
    """
    df = pd.read_sql(query, engine)
    # İndirim oranını yüzdeye çevir
    df['discount_percent'] = df['discount'] * 100
    return df

def add_return_risk_label(df):
    """
    Hedef değişkeni ekler: return_risk
    - Yüksek indirim (%20'den fazla) ve düşük harcama (<$100) olan siparişler riskli
    """
    high_discount = df['discount_percent'] > 20
    low_amount = df['total_amount'] < 100
    df['return_risk'] = (high_discount & low_amount).astype(int)
    return df

def prepare_return_risk_data():
    """
    Model için kullanılacak veri setini hazırlar.
    """
    df = get_order_features()
    df = add_return_risk_label(df)
    # Kullanılacak özellikler ve hedef değişken
    features = [
        'quantity',
        'unit_price',
        'discount',
        'total_amount',
        'discount_percent'
    ]
    return df[features + ['return_risk']]

# Test ve örnek çıktı
if __name__ == "__main__":
    df = prepare_return_risk_data()
    print("\nİade Riski Veri Seti:")
    print(df.head())




## 2. Ürün İade Risk Skoru Modeli

### Veri Hazırlama

#- Order Details tablosundan indirim, miktar ve toplam tutar bilgileri çekilecek
#- Yüksek indirim + düşük harcama mantığıyla sentetik iade etiketleri oluşturulacak


### Model Geliştirme

#- Özellik mühendisliği: İndirim değerleri normalize edilecek, birim başına fiyat hesaplanacak
#- Derin öğrenme modeli oluşturulacak
#- Düzenlileştirme (regularization) uygulanacak

### Ar-Ge Konuları: 

# Recommendation Systems: Deep Learning tabanlı ürün öneri sistemleri araştır (örneğin Neural Collaborative Filtering, AutoEncoders).
# Multi-label Prediction: Aynı anda birkaç ürünü birden önerebilecek bir sistem geliştir.

### Ar-Ge Konuları

#- Maliyet-duyarlı Öğrenme: Yanlış negatifleri daha fazla cezalandıran özel kayıp fonksiyonu
#- Açıklanabilir Yapay Zeka: SHAP veya LIME ile model yorumlaması

### API Uygulaması

#- Endpoint: `/return_risk`
#- Girdi: Sipariş detayları (ürünler, miktarlar, indirimler)
#- Çıktı: Risk skoru ve etki eden faktörler