from django.contrib import admin
from .models import Movie, Favorite, Genre, Review, ReviewComment, ReviewLike, WatchHistory


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'imdb_rating', 'get_genres', 'director')
    search_fields = ('id', 'title', 'genres__name')
    list_filter = ('release_date', 'genres')
    filter_horizontal = ('genres',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Genres'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('user', 'movie')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at', 'comment')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('rating', 'created_at')


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at')
    search_fields = ('user__username', 'review__movie__title', 'review__user__username')
    list_filter = ('created_at',)


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'review')
    search_fields = ('user__username', 'review__movie__title', 'review__user__username')
    list_filter = ('user',)


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'watched_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('watched_at',)
