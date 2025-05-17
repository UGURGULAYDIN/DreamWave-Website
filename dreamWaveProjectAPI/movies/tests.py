import os
from django.conf import settings

# Ayarları doğru şekilde yüklemek için ortam değişkenini ayarlayın
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dreamWaveProject.settings')

# Django'yu başlatmak
import django

django.setup()

import re
import pandas as pd
import requests
from django.shortcuts import get_object_or_404
from movies.models import Movie
from users.models import User

# Django server ayarları
BASE_URL = "http://127.0.0.1:8000/"  # Django server adresi

# Klasör yolları
eslesen_yorumlar_klasoru = "C:/Users/acer/Desktop/eslesen_yorumlar"


def validate_rating(rating_value):
    """Rating değerini geçerli bir sayıya dönüştür."""
    rating_str = str(rating_value).strip()  # Rating'i string'e çevir ve boşlukları temizle

    if rating_str.replace('.', '', 1).isdigit():  # Virgül veya nokta olabilir
        try:
            rating = float(rating_str)  # Eğer geçerli bir sayıysa, float'a çevir
            return int(rating)  # Sayıyı tamsayıya çevir
        except ValueError:
            print(f"⚠️ Rating değeri geçerli değil: {rating_value}")
            return None
    else:
        print(f"⚠️ Geçersiz rating: {rating_value}")
        return None


def register_user(username, email, password):
    """Kullanıcı kaydını gerçekleştirir."""
    register_url = f"{BASE_URL}/api/register/"
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        register_response = requests.post(register_url, json=user_data)
        if register_response.status_code == 201:
            print(f"✅ Kullanıcı oluşturuldu: {username}")
        elif register_response.status_code == 400:
            print(f"⚠️ Kullanıcı zaten var: {username}")
        else:
            print(f"❌ Kullanıcı kaydı başarısız: {username} -> {register_response.text}")
    except Exception as e:
        print(f"❌ Kullanıcı kaydı hatası: {username} -> {e}")


def post_review(username, film_adi, rating, comment):
    """Yorumu API'ye gönderir."""
    # Kullanıcıyı ve filmi veritabanından al
    users = User.objects.filter(username=username)

    if users.count() == 1:
        user = users.first()
    else:
        print(f"⚠️ Kullanıcı bulunamadı veya birden fazla kullanıcı bulundu: {username}")
        return

    movie = Movie.objects.filter(title=film_adi).first()
    if not movie:
        print(f"⚠️ Film bulunamadı: {film_adi}")
        return

    review_url = f"{BASE_URL}/api/reviews/"
    review_data = {
        "user_id": user.id,  # user_id kullanılıyor
        "movie_id": movie.id,  # movie_id kullanılıyor
        "rating": rating,
        "comment": comment
    }

    try:
        review_response = requests.post(review_url, json=review_data)
        if review_response.status_code == 201:
            print(f"✅ Yorum yapıldı: {username} -> {film_adi}")
        else:
            print(f"❌ Yorum başarısız: {username} -> {film_adi} -> {review_response.text}")
    except Exception as e:
        print(f"❌ Yorum gönderme hatası: {username} -> {film_adi} -> {e}")


def process_csv_file(dosya_yolu):
    """CSV dosyasını işle ve verileri Django'ya gönder."""
    try:
        df = pd.read_csv(dosya_yolu)
    except Exception as e:
        print(f"❌ Hata oluştu dosya okunurken: {dosya_yolu} -> {e}")
        return

    for index, row in df.iterrows():
        username = str(row['username']).strip()
        rating_value = row['rating']
        comment = str(row['review']).strip()

        # Rating değerini doğrula
        rating = validate_rating(rating_value)
        if rating is None:
            continue  # Geçersiz rating varsa, bu satırı atla

        # Kullanıcı bilgileri
        email = f"{username.lower()}@dreamwave.com"
        password = "defaultpassword123"

        # Kullanıcıyı kaydet
        register_user(username, email, password)

        # Yorumu gönder
        film_adi_raw = os.path.basename(dosya_yolu)[:-4]  # Dosya adını al, ".csv" uzantısını sil
        film_adi = re.sub(r'\s\d{4}$', '', film_adi_raw)  # Yılı kaldır
        post_review(username, film_adi, rating, comment)


def process_all_csv_files():
    """Tüm CSV dosyalarını işle."""
    yorum_dosyalari = [f for f in os.listdir(eslesen_yorumlar_klasoru) if f.endswith('.csv')]

    for dosya in yorum_dosyalari:
        dosya_yolu = os.path.join(eslesen_yorumlar_klasoru, dosya)
        process_csv_file(dosya_yolu)


if __name__ == "__main__":
    process_all_csv_files()
