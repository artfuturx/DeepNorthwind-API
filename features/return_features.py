import pandas as pd
from data.database_connect import get_db_engine

def get_return_risk_features():
    engine = get_db_engine()
    query = """
    SELECT
        od."OrderID",
        od."ProductID",
        od."UnitPrice",
        od."Quantity",
        od."Discount",
        (od."UnitPrice" * od."Quantity" * (1 - od."Discount")) AS total_price,
        -- Sentetik iade etiketi: yüksek indirim ve düşük harcama
        CASE
            WHEN od."Discount" > 0.2 AND (od."UnitPrice" * od."Quantity" * (1 - od."Discount")) < 100 THEN 1
            ELSE 0
        END AS is_returned
    FROM "Order Details" od
    """
    df = pd.read_sql(query, engine)
    return df



## 2. Ürün İade Risk Skoru Modeli

### Veri Hazırlama

#- Order Details tablosundan indirim, miktar ve toplam tutar bilgileri çekilecek
#- Yüksek indirim + düşük harcama mantığıyla sentetik iade etiketleri oluşturulacak

### Model Geliştirme

#- Özellik mühendisliği: İndirim değerleri normalize edilecek, birim başına fiyat hesaplanacak
#- Derin öğrenme modeli oluşturulacak
#- Düzenlileştirme (regularization) uygulanacak

### Ar-Ge Konuları

#- Maliyet-duyarlı Öğrenme: Yanlış negatifleri daha fazla cezalandıran özel kayıp fonksiyonu
#- Açıklanabilir Yapay Zeka: SHAP veya LIME ile model yorumlaması

### API Uygulaması

#- Endpoint: `/return_risk`
#- Girdi: Sipariş detayları (ürünler, miktarlar, indirimler)
#- Çıktı: Risk skoru ve etki eden faktörler