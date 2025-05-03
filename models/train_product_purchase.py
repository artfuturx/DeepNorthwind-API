"""
Dosya Adı: models/train_product_purchase.py
Amaç: Ürün satın alma potansiyeli tahmin modelini eğitmek için kullanılır.
Yapılanlar: Ürün özellikleri kullanılarak, ürünün satın alma potansiyeli tahmin edilir.
Kullanılan Algoritma: TensorFlow kullanılarak derin öğrenme (Deep Learning) modeli, özellikle çok katmanlı sinir ağı (Multi-layer Perceptron) kullanılmıştır.
Sonuçların Kaydedilmesi: Eğitilen model ve ölçekleyici (scaler) 'saved_models/product_purchase' dizinine kaydedilir.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import joblib
import os

from features.product_features import prepare_purchase_potential_data

# 1. Veri Hazırlama
df = prepare_purchase_potential_data()

# Sadece sayısal sütunları seç
exclude_cols = ['customer_id', 'company_name', 'category_name', 'recent_purchase', 'last_order_date']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
print("Modelde kullanılacak sütunlar:", feature_cols)

X = df[feature_cols].fillna(0)
y = df['recent_purchase']

print("Modelde kullanılacak sütunlar:", feature_cols)
print(X.dtypes)

# 2. Veri Ölçekleme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Eğitim/Test bölme
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 4. Model Kurulumu
model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 5. Model Eğitimi
model.fit(X_train, y_train, epochs=30, batch_size=16, validation_split=0.2)

# 6. Model ve Scaler Kaydetme
save_dir = 'saved_models/product_purchase'
os.makedirs(save_dir, exist_ok=True)
model.save(os.path.join(save_dir, 'product_purchase_model.h5'))
joblib.dump(scaler, os.path.join(save_dir, 'scaler.pkl'))

# 7. Test Sonucu
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.2f}")

# Kullanım örneği
def predict_purchase_potential(new_data):
    X_new = scaler.transform(new_data[feature_cols].fillna(0))
    prob = model.predict(X_new)
    return prob

if __name__ == "__main__":
    print("Model ve scaler başarıyla kaydedildi.") 
    print("Modelde kullanılacak sütunlar:", feature_cols)