import pandas as pd
from features.customer_features import get_customer_order_features
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

def main():
    # 1. Özellikleri çek
    df = get_customer_order_features()

    # 2. Dummy hedef değişken (örnek amaçlı, gerçek projede gerçek etiket olmalı)
    # Burada: son sipariş tarihi 2023'ten önce olanlar 0, sonra olanlar 1 gibi basit bir kural
    df["reordered_in_6_months"] = (pd.to_datetime(df["last_order_date"]) > "2023-06-01").astype(int)

    # 3. Özellik ve hedef seçimi
    X = df[["total_orders", "total_spent", "avg_order_value"]]
    y = df["reordered_in_6_months"]

    # 4. Eğitim/test bölmesi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Model eğitimi
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 6. Tahmin ve değerlendirme
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # 7. Görselleştirme: Confusion Matrix
    disp = ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
    plt.title("Confusion Matrix")
    plt.show()

    # 8. Özelliklerin dağılımı (örnek görselleştirme)
    df.boxplot(column="total_spent", by="reordered_in_6_months")
    plt.title("Total Spent by Reorder Status")
    plt.suptitle("")
    plt.xlabel("Reordered in 6 Months")
    plt.ylabel("Total Spent")
    plt.show()

if __name__ == "__main__":
    main()