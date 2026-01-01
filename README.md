# Banka Müşteri Harcama Analizi ve Segmentasyon Projesi

Bu proje, Python kullanarak sentetik banka müşteri verileri üzerinde veri analizi, SQL sorgulama ve müşteri segmentasyonu (K-Means) işlemlerini gerçekleştirmektedir.

## 📂 Proje Yapısı

- `data_generator.py`: Müşteri ve işlem verilerini rastgele (ancak mantıklı dağılımlarla) oluşturur.
- `main_analysis.py`: Veri temizleme, görselleştirme, SQL analizi ve ML segmentasyonunu içerir.
- `customers.csv` & `transactions.csv`: Oluşturulan veri setleri.
- `*.png`: Analiz sonucu üretilen grafikler.

## 🚀 Kurulum ve Çalıştırma

Gerekli kütüphanelerin yüklü olduğundan emin olun:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

1. **Veri Üretme:**
   ```bash
   python BankCustomerAnalysis/data_generator.py
   ```
   Bu işlem `customers.csv` ve `transactions.csv` dosyalarını oluşturur.

2. **Analizi Çalıştırma:**
   ```bash
   python BankCustomerAnalysis/main_analysis.py
   ```
   Bu komut çıktıda analiz sonuçlarını gösterir ve grafikleri kaydeder.

## 📊 Analiz Adımları ve Sonuçlar

### 1. Veri Temizleme
- Eksik veriler kontrol edildi.
- Tarih formatları düzeltildi.
- Müşteri ve İşlem tabloları birleştirildi.

### 2. Keşifsel Veri Analizi (EDA)
Kod çalıştırıldığında aşağıdaki görseller üretilir:
- **`monthly_trend.png`**: Aylık toplam harcama trendi.
- **`category_spending.png`**: Market, Elektronik vb. kategorilerin dağılımı.
- **`age_group_spending.png`**: Yaş gruplarına göre harcama alışkanlıkları.

**Örnek İçgörü:** 26-35 yaş aralığındaki müşterilerin ortalama işlem tutarı diğer gruplara göre daha yüksektir (Elektronik harcamalarının yoğunluğu nedeniyle).

### 3. SQL ile Analitik Sorgular
Python içindeki `sqlite3` kullanılarak aşağıdaki sorulara cevap arandı:
- **En çok harcama yapan ilk 10 müşteri:** (VIP müşteri potansiyeli)
- **Şehir bazlı ortalama harcama:** (Bölgesel kampanya planlaması için)

### 4. Müşteri Segmentasyonu (K-Means)
Müşteriler; Toplam Harcama, İşlem Sayısı ve Ortalama Sepet Tutarı metriklerine göre 4 segmente ayrıldı.

| Segment | Tanım | Aksiyon Önerisi |
|---------|-------|-----------------|
| **Cluster 0** | Orta Harcama - Sık İşlem | Sadakat programlarına dahil edilebilir. |
| **Cluster 1** | Orta Harcama - Seyrek İşlem | İşlem sıklığını artırıcı (ör: 3. harcamaya indirim) kampanyalar. |
| **Cluster 2** | **Yüksek Değerli (VIP)** | Özel müşteri temsilcisi atanmalı, premium kart teklif edilmeli. |
| **Cluster 3** | Düşük Harcama - Seyrek İşlem | Kayıp riski yüksek, "Win-back" kampanyaları denenebilir. |

*(Not: Cluster numaraları her çalıştırmada değişebilir, yukarıdaki tablo örnek yorumlamadır.)*
