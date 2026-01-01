import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Set visualization style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_and_clean_data():
    print("--- 1. VERİ TEMİZLEME VE YÜKLEME ---")

    # Load Data
    try:
        df_cust = pd.read_csv('BankCustomerAnalysis/customers.csv')
        df_tx = pd.read_csv('BankCustomerAnalysis/transactions.csv')
    except FileNotFoundError:
        print("Hata: CSV dosyaları bulunamadı. Lütfen önce data_generator.py çalıştırın.")
        return None, None

    # Date Conversion
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])

    # Check for missing values
    print("Müşteri verisi eksik değerler:\n", df_cust.isnull().sum())
    print("İşlem verisi eksik değerler:\n", df_tx.isnull().sum())

    # Merge for easier analysis
    df_merged = df_tx.merge(df_cust, on='customer_id', how='left')

    print(f"Veri yüklendi: {len(df_cust)} müşteri, {len(df_tx)} işlem.")
    return df_merged, df_cust, df_tx

def perform_eda(df_merged):
    print("\n--- 2. KEŞİFSEL VERİ ANALİZİ (EDA) ---")

    # 1. Monthly Spending Trend
    df_merged['month_year'] = df_merged['transaction_date'].dt.to_period('M')
    monthly_trend = df_merged.groupby('month_year')['amount'].sum().reset_index()
    monthly_trend['month_year'] = monthly_trend['month_year'].astype(str)

    plt.figure()
    sns.lineplot(data=monthly_trend, x='month_year', y='amount', marker='o')
    plt.xticks(rotation=45)
    plt.title('Aylık Toplam Harcama Trendi')
    plt.xlabel('Ay')
    plt.ylabel('Toplam Harcama (TL)')
    plt.tight_layout()
    plt.savefig('BankCustomerAnalysis/monthly_trend.png')
    print("Grafik kaydedildi: monthly_trend.png")

    # 2. Category Distribution
    plt.figure()
    cat_sum = df_merged.groupby('category')['amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=cat_sum, x='category', y='amount', palette='viridis', hue='category', legend=False)
    plt.title('Kategorilere Göre Toplam Harcama')
    plt.ylabel('Harcama (TL)')
    plt.savefig('BankCustomerAnalysis/category_spending.png')
    print("Grafik kaydedildi: category_spending.png")

    # 3. Age Group Analysis
    # Create age bins
    bins = [18, 25, 35, 50, 70, 100]
    labels = ['18-25', '26-35', '36-50', '51-70', '70+']
    df_merged['age_group'] = pd.cut(df_merged['age'], bins=bins, labels=labels, right=False)

    age_group_spend = df_merged.groupby('age_group', observed=True)['amount'].mean().reset_index()

    plt.figure()
    sns.barplot(data=age_group_spend, x='age_group', y='amount', palette='magma', hue='age_group', legend=False)
    plt.title('Yaş Gruplarına Göre Ortalama İşlem Tutarı')
    plt.ylabel('Ortalama Tutar (TL)')
    plt.savefig('BankCustomerAnalysis/age_group_spending.png')
    print("Grafik kaydedildi: age_group_spending.png")

    # Insight Example
    max_spend_age = age_group_spend.sort_values(by='amount', ascending=False).iloc[0]
    print(f"İçgörü: En yüksek ortalama harcama {max_spend_age['age_group']} yaş grubunda ({max_spend_age['amount']:.2f} TL).")

def run_sql_queries(df_cust, df_tx):
    print("\n--- 3. SQL ANALİTİK SORGULAR ---")

    # Setup in-memory SQLite
    conn = sqlite3.connect(':memory:')
    df_cust.to_sql('customers', conn, index=False)
    df_tx.to_sql('transactions', conn, index=False)

    cursor = conn.cursor()

    # Query 1: Top 10 Customers by Total Spending
    print("Sorgu 1: En Çok Harcama Yapan İlk 10 Müşteri")
    query1 = """
    SELECT
        c.customer_id,
        c.city,
        COUNT(t.transaction_id) as tx_count,
        ROUND(SUM(t.amount), 2) as total_spend
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id
    ORDER BY total_spend DESC
    LIMIT 10;
    """
    res1 = pd.read_sql_query(query1, conn)
    print(res1)

    # Query 2: Average Spending by City
    print("\nSorgu 2: Şehir Bazlı Ortalama Harcama")
    query2 = """
    SELECT
        c.city,
        ROUND(AVG(t.amount), 2) as avg_tx_amount,
        ROUND(SUM(t.amount), 2) as total_city_spend
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.city
    ORDER BY avg_tx_amount DESC;
    """
    res2 = pd.read_sql_query(query2, conn)
    print(res2)

    conn.close()

def perform_segmentation(df_merged):
    print("\n--- 4. MÜŞTERİ SEGMENTASYONU (K-MEANS) ---")

    # Aggregate data per customer for clustering
    customer_metrics = df_merged.groupby('customer_id').agg({
        'amount': ['sum', 'mean', 'count']
    })

    # Flatten columns
    customer_metrics.columns = ['total_spend', 'avg_spend', 'tx_count']
    customer_metrics = customer_metrics.reset_index()

    # Standardization
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(customer_metrics[['total_spend', 'avg_spend', 'tx_count']])

    # K-Means Clustering (Let's use K=4)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_metrics['cluster'] = kmeans.fit_predict(scaled_features)

    # Analyze Clusters
    cluster_summary = customer_metrics.groupby('cluster').agg({
        'total_spend': 'mean',
        'avg_spend': 'mean',
        'tx_count': 'mean',
        'customer_id': 'count'
    }).reset_index()

    print("Segmentasyon Sonuçları (Ortalama Değerler):")
    print(cluster_summary)

    # Assign logic names to clusters (Just a heuristic based on the run)
    # We will print the interpretation dynamically based on values
    print("\nSegment Yorumları:")
    for index, row in cluster_summary.iterrows():
        print(f"Cluster {int(row['cluster'])}: {int(row['customer_id'])} müşteri -> "
              f"Ort. Toplam: {row['total_spend']:.1f} TL, "
              f"Ort. İşlem Sayısı: {row['tx_count']:.1f}")

    # Visualize Clusters
    plt.figure()
    sns.scatterplot(data=customer_metrics, x='tx_count', y='total_spend', hue='cluster', palette='deep', s=60)
    plt.title('Müşteri Segmentleri: İşlem Sayısı vs Toplam Harcama')
    plt.xlabel('İşlem Sayısı')
    plt.ylabel('Toplam Harcama')
    plt.legend(title='Segment')
    plt.savefig('BankCustomerAnalysis/segmentation_clusters.png')
    print("Grafik kaydedildi: segmentation_clusters.png")

    return customer_metrics

if __name__ == "__main__":
    df_full, df_c, df_t = load_and_clean_data()
    if df_full is not None:
        perform_eda(df_full)
        run_sql_queries(df_c, df_t)
        perform_segmentation(df_full)
