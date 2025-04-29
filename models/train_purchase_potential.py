import pandas as pd
from features.product_features import get_product_purchase_potential_features
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

def main():
    # 1. Özellikleri çek
    df = get_product_purchase_potential_features()

    # 2. Dummy hedef değişken (örnek amaçlı, gerçek projede gerçek etiket olmalı)
    # Örneğin: toplam harcama > 500 ise 1, değilse 0
    df["high_potential"] = (df["total_spent_on_category"] > 500).astype(int)

    # 3. Kategorileri one-hot encode et
    X = pd.get_dummies(df[["total_spent_on_category", "order_count_in_category", "avg_price_in_category", "CategoryName"]])
    y = df["high_potential"]

    # 4. Eğitim/test bölmesi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Model eğitimi
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # 6. Tahmin ve değerlendirme
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # 7. Görselleştirme: Confusion Matrix
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
    plt.title("Confusion Matrix")
    plt.show()

    # 8. Kategoriye göre harcama dağılımı
    df.boxplot(column="total_spent_on_category", by="CategoryName", rot=90)
    plt.title("Total Spent by Category")
    plt.suptitle("")
    plt.xlabel("Category")
    plt.ylabel("Total Spent")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()