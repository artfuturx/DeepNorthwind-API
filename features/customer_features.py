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


## 1. Müşteri Sipariş Verme Tahmini Modeli

### Veri Hazırlama

#- Orders, Order Details ve Customers tablolarından veri çekilecek
#- Müşteri başına toplam harcama hesaplanacak
#- Sipariş sayısı ve ortalama sipariş büyüklüğü hesaplanacak
#- Son sipariş tarihinden itibaren geçen süre hesaplanacak
#- Mevsimsellik özellikleri çıkarılacak (ay bazında)

### Ar-Ge Konuları: 

#Temporal Features: Mevsimsellik etkisi var mı? (Örn: Yaz aylarında sipariş artıyor mu?)
#Data Augmentation: Müşteri datasını arttırarak daha büyük bir veri seti oluşturup modelin başarısını gözlemle.
#Class Imbalance: Eğer az kişi sipariş veriyorsa, class_weight veya SMOTE gibi yöntemlerle çözüm üret.

### Model Geliştirme

#- Hedef değişken: Müşterinin son siparişinden sonraki 6 ay içinde tekrar sipariş verip vermediği
#- Veri eğitim ve test setlerine bölünecek
#- TensorFlow/Keras kullanılarak derin öğrenme modeli oluşturulacak

### Ar-Ge Konuları

#- Zamansal Özllikler: Sipariş ayı/mevsimi etkileri analiz edilecek
#- Veri Artırma: SMOTE gibi tekniklerle müşteri verileri çoğaltılacak
#- Sınıf Dengesizliği: class_weight parametresi kullanılacak

### API Uygulaması

#- Endpoint: `/predict_reorder`
#- Girdi: Müşteri ID
#- Çıktı: Önümüzdeki 6 ay içinde sipariş verme olasılığı