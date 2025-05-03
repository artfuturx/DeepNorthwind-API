# DeepNorthwind-API

## Proje Amacı
Bu proje, Northwind veritabanı üzerinde makine öğrenmesi modelleri kullanarak müşteri yeniden sipariş tahmini, ürün satın alma potansiyeli tahmini ve iade riski tahmini yapmayı amaçlamaktadır. Bu tahminler, işletmelerin müşteri davranışlarını anlamalarına ve stratejik kararlar almalarına yardımcı olur.

## Proje Geliştiricisi
Bu proje, [SEVGİ BERK SÜTBAŞ](https://github.com/artfuturx) tarafından Turkcell GYK1 projeleri kapsamında geliştirilmiştir.

## Proje Adımları
1. **Veri Hazırlama**: Müşteri, ürün ve iade verilerinden özellik çıkarımı yapılır. Bu adımda, verilerin temizlenmesi, dönüştürülmesi ve özellik mühendisliği yapılır.
2. **Model Eğitimi**: TensorFlow kullanılarak derin öğrenme modelleri eğitilir. Bu modeller, veri seti üzerinde eğitilerek tahmin yapabilir hale getirilir.
3. **API Geliştirme**: FastAPI kullanılarak tahmin yapmak için API endpoint'leri oluşturulur. Bu endpoint'ler, kullanıcıların model tahminlerini alabilmelerini sağlar.

## Dosya Yapısı
```
DeepNorthwind-API/
├── data/
│   └── database_connect.py
├── features/
│   ├── customer_features.py
│   ├── product_features.py
│   └── return_features.py
├── models/
│   ├── train_customer_reorder.py
│   ├── train_product_purchase.py
│   └── train_return_risk.py
├── saved_models/
│   ├── customer_reorder/
│   ├── product_purchase/
│   └── return_risk/
├── images/
│   └── (model performans grafikleri, veri dağılım grafikleri)
└── README.md
```

## Dosyaların İçeriği
- **data/database_connect.py**: Northwind veritabanına bağlantı sağlar ve temel tablo sorgularını yapar. Bu dosya, veritabanı bağlantısını kurar ve gerekli verileri çeker.
- **features/customer_features.py**: Müşteri verilerinden özellik çıkarımı yapar. Bu dosya, müşteri sipariş geçmişi, sipariş sıklığı, ortalama sipariş tutarı gibi özellikleri çıkarır.
- **features/product_features.py**: Ürün verilerinden özellik çıkarımı yapar. Bu dosya, ürün satış geçmişi, stok durumu, fiyat bilgisi gibi özellikleri çıkarır.
- **features/return_features.py**: İade verilerinden özellik çıkarımı yapar. Bu dosya, iade geçmişi, sipariş detayları, müşteri bilgileri gibi özellikleri çıkarır.
- **models/train_customer_reorder.py**: Müşteri yeniden sipariş tahmin modelini eğitir. Bu dosya, müşteri özelliklerini kullanarak, müşterinin yeniden sipariş verip vermeyeceğini tahmin eder.
- **models/train_product_purchase.py**: Ürün satın alma potansiyeli tahmin modelini eğitir. Bu dosya, ürün özelliklerini kullanarak, ürünün satın alma potansiyelini tahmin eder.
- **models/train_return_risk.py**: İade riski tahmin modelini eğitir. Bu dosya, iade özelliklerini kullanarak, iade riskini tahmin eder.

## API Endpoint'leri
- **Görsel**: [Tüm Tahminler Grafiği](images/predict_all_graph.png)
- **/customer_reorder**: Müşteri yeniden sipariş tahmini yapar. Bu endpoint, müşteri ID'si ve sipariş detayları alarak, müşterinin yeniden sipariş verip vermeyeceğini tahmin eder.
  - **Görsel**: [Müşteri Yeniden Sipariş Tahmini Grafiği](images/customer_reorder_graph.png)
- **/product_purchase**: Ürün satın alma potansiyeli tahmini yapar. Bu endpoint, ürün ID'si ve müşteri detayları alarak, ürünün satın alma potansiyelini tahmin eder.
  - **Görsel**: [Ürün Satın Alma Potansiyeli Grafiği](images/product_purchase_graph.png)
- **/return_risk**: İade riski tahmini yapar. Bu endpoint, sipariş detayları alarak, iade riskini tahmin eder.
  - **Görsel**: [İade Riski Grafiği](images/return_risk_graph.png)

## Images Dosyasındaki Resimlerin Kullanımı
Images dosyasındaki resimler, projenin görselleştirme ve raporlama amaçları için kullanılır. Örneğin, model performans grafikleri veya veri dağılım grafikleri burada saklanabilir. Bu grafikler, model performansını ve veri dağılımını görselleştirmek için kullanılır.
