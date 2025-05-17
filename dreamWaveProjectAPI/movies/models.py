from django.db import models
from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.AutoField(primary_key=True)  # ID
    title = models.CharField(max_length=255)  # Film Adı
    description = models.TextField()  # Açıklama
    release_date = models.DateField()  # Yayınlanma Tarihi
    imdb_rating = models.FloatField()  # IMDb Puanı
    poster_url = models.URLField()  # Afiş URL'si
    video_url = models.URLField(blank=True, null=True)  # Film URL'si
    genres = models.ManyToManyField(Genre)  # Türü
    director = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')  # Aynı filmi iki kez eklemesin

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')  # Yorumu yapan kullanıcı
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')  # Yorum yapılan film
    rating = models.PositiveIntegerField()  # 1-10 arası puan
    comment = models.TextField(blank=True, null=True)  # İsteğe bağlı yorum
    created_at = models.DateTimeField(auto_now_add=True)  # Otomatik tarih

    class Meta:
        unique_together = ('user', 'movie')  # Kullanıcı her filme 1 kez yorum yapabilsin

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title} [{self.rating}]"


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.review}"


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('review', 'user')  # Her kullanıcı sadece 1 kez beğenebilsin

    def __str__(self):
        return f"{self.user.username} liked {self.review}"


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Aynı film bir kez izlenmiş sayılır

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title}"
