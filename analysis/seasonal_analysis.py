import pandas as pd
import matplotlib.pyplot as plt
from data.database_connect import engine

query = """
SELECT order_date
FROM orders
"""
df = pd.read_sql(query, engine)
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.month

monthly_counts = df['month'].value_counts().sort_index()

plt.figure(figsize=(8,5))
plt.bar(monthly_counts.index, monthly_counts.values, color='skyblue')
plt.xlabel('Ay')
plt.ylabel('Sipariş Sayısı')
plt.title('Aylara Göre Sipariş Dağılımı')
plt.xticks(range(1,13))
plt.show()