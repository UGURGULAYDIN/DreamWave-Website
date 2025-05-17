from rest_framework import serializers
from .models import Movie, Favorite, Genre, Review, ReviewComment, ReviewLike, WatchHistory


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), write_only=True, source='genres'
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'imdb_rating', 'director', 'poster_url', 'video_url',
                  'genres', 'genre_ids']


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'movie']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), source='movie')

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'movie_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'movie']


class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    review_id = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), source='review', write_only=True)

    class Meta:
        model = ReviewComment
        fields = ['id', 'user', 'review_id', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    review_id = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), source='review', write_only=True)

    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review_id']
        read_only_fields = ['id', 'user']


class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'movie', 'watched_at']
