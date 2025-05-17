# 🎬 DreamWave

**DreamWave**, modern ve yapay zekâ destekli bir film izleme platformudur. Kullanıcıların film/dizi içeriklerini keşfetmesini, yorum yapmasını, öneri almasını ve izleme listeleri oluşturmasını sağlar.


## 🚀 Özellikler

- 🧠 **Yapay Zekâ Destekli Film Öneri Sistemi**
- 💬 **Yorumlardan AI ile Otomatik Özetleme**
- ⭐ **Kullanıcı Puanlama ve Geri Bildirim Sistemi**
- 📺 **Film İzleme Geçmişi ve Favorilere Ekleme**
- 🔎 **Gelişmiş Arama ve Filtreleme (IMDb puanı, tür vs.)**
- 📱 **Responsive ve Modern Arayüz**

---

## 🖼️ Uygulama Görselleri

### 🏠 Ana Sayfa
![Image](https://github.com/user-attachments/assets/76a0da7a-d64e-4b37-b40c-6e3e6d13e167)

### 🎞️ Film Detay Sayfası
![Image](https://github.com/user-attachments/assets/b7addb6a-973d-4688-a4c5-ce344b082a40)
![Image](https://github.com/user-attachments/assets/3ffe0527-d96a-41d7-bffb-d22614572d01)

### 👤 Kullanıcı Profili
![Image](https://github.com/user-attachments/assets/59b474ed-4710-421b-944f-47708537687c)
![Image](https://github.com/user-attachments/assets/23bba8f9-c222-457e-87e9-e7075c208f37)

### 🔍 Arama Sayfası
![Image](https://github.com/user-attachments/assets/719453b4-2e80-4419-8bf4-1b8b488adbd7)

### 🔐 Giriş ve Kayıt Sayfası
![Giriş Sayfası](https://github.com/user-attachments/assets/bfb8f4cb-3c84-4598-a909-c6249b31f55b)
![Kayıt Sayfası](https://github.com/user-attachments/assets/715184b6-a516-4b0b-a3ec-852cd9a7c3c2)

---

## ⚙️ Teknolojiler

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript
- **Makine Öğrenimi:** TF-IDF, Cosine Similarity, Open Source LLM (Local Model)
- **Veritabanı:** SQLite
- **API Entegrasyonları:** Custom REST API endpoint’leri

---

## 🧠 Yapay Zekâ Destekli Özellikler

### 🎯 Film Öneri Sistemi
Kullanıcının izleme geçmişi, favorileri ve yaptığı yorumlara göre içerikler arasında benzerlik analizi yapılarak **kişiselleştirilmiş film önerileri** sunulur.

### 📝 Yorum Özetleme
Her filmde yer alan kullanıcı yorumları doğal dil işleme yöntemleri ile analiz edilerek, **genel görüşü yansıtan otomatik özet metinleri** oluşturulur.

---

## 🔧 Kurulum (Yerel)

1. Reposu klonlayın:
```bash
git clone https://github.com/kullanici-adi/dreamwave.git
```

2. Sanal ortam oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # (Windows için: venv\Scripts\activate)
```
3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```
4. Veritabanını oluşturun:
```bash
python manage.py migrate
```
5. Sunucuyu başlatın:
```bash
python manage.py runserver
```

---

## 📌 Yol Haritası
-  Favorilere ekleme / kaldırma

-  İzleme geçmişi kaydı

-  Gelişmiş yorum ve beğeni sistemi

-  Yapay zekâ destekli film öneri sistemi

-  Yorumlardan genel görüş çıkarımı

-  Sosyal medya paylaşımı

-  İzleme grupları oluşturma

---

## 🧑‍💻 Geliştirici
**Linkedin:** https://www.linkedin.com/in/u%C4%9Fur-g%C3%BClaydin-9053902b6/

---

## 📄 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına göz atabilirsiniz.
