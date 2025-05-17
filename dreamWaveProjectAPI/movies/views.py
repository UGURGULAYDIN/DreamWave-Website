from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Movie, Favorite, Review, ReviewComment, ReviewLike, WatchHistory
from users.models import User
from .serializers import MovieSerializer, FavoriteSerializer, ReviewSerializer, ReviewCommentSerializer, \
    WatchHistorySerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.decorators import api_view
import numpy as np
from transformers import pipeline


class MovieCreateAPIView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        search = request.query_params.get("search")
        min_rating = request.query_params.get("min_rating")
        genre = request.query_params.get("genre")  # yeni

        if search:
            movies = movies.filter(Q(title__icontains=search))

        if min_rating:
            try:
                min_rating = float(min_rating)
                movies = movies.filter(imdb_rating__gte=min_rating)
            except ValueError:
                pass

        if genre:
            movies = movies.filter(genres__name__icontains=genre)

        serializer = MovieSerializer(movies.distinct(), many=True)
        return Response(serializer.data)


class MovieDetailAPIView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [AllowAny]  # Doğrulama olmadığı için herkese açık

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Favorite.objects.none()
        return Favorite.objects.filter(user_id=user_id)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        movie_id = request.data.get('movie_id')

        if not user_id or not movie_id:
            return Response({'error': 'user_id ve movie_id gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Kullanıcı bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Film bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=user, movie=movie)

        if not created:
            return Response({'message': 'Bu film zaten favorilerde.'}, status=status.HTTP_200_OK)

        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)


class UserFavoriteListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


class FavoriteDeleteView(APIView):
    def delete(self, request):
        user_id = request.data.get("user_id")
        movie_id = request.data.get("movie_id")

        if not user_id or not movie_id:
            return Response({'error': 'user_id ve movie_id gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = Favorite.objects.get(user_id=user_id, movie_id=movie_id)
            favorite.delete()
            return Response({'message': 'Favori başarıyla kaldırıldı.'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favori bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        serializer.save(user=user)


class ReviewCommentCreateView(APIView):
    def post(self, request, review_id):
        user_id = request.data.get("user_id")
        comment = request.data.get("comment")

        if not user_id or not comment:
            return Response({"error": "user_id ve comment zorunludur."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        review = get_object_or_404(Review, id=review_id)

        new_comment = ReviewComment.objects.create(
            review=review,
            user=user,
            comment=comment
        )

        serializer = ReviewCommentSerializer(new_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewCommentListView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = ReviewComment.objects.filter(review=review).order_by('-created_at')
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data)


class ReviewLikeToggleView(APIView):
    def post(self, request, review_id):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id zorunludur."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        review = get_object_or_404(Review, id=review_id)

        existing_like = ReviewLike.objects.filter(user=user, review=review).first()

        if existing_like:
            existing_like.delete()
            return Response({"message": "Beğeni kaldırıldı."}, status=status.HTTP_200_OK)
        else:
            ReviewLike.objects.create(user=user, review=review)
            return Response({"message": "Yorum beğenildi."}, status=status.HTTP_201_CREATED)


class ReviewLikeCountView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        count = ReviewLike.objects.filter(review=review).count()
        return Response({'likes': count})


class ReviewLikeUserListView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        likes = ReviewLike.objects.filter(review=review)
        user_ids = likes.values_list('user_id', flat=True)
        return Response({'users': list(user_ids)})


class WatchHistoryCreateView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        movie_id = request.data.get('movie_id')

        if not user_id or not movie_id:
            return Response({'error': 'user_id ve movie_id gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            movie = Movie.objects.get(id=movie_id)
        except (User.DoesNotExist, Movie.DoesNotExist):
            return Response({'error': 'Kullanıcı veya film bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        history, created = WatchHistory.objects.get_or_create(user=user, movie=movie)
        serializer = WatchHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class WatchHistoryListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        history = WatchHistory.objects.filter(user=user).order_by('-watched_at')
        serializer = WatchHistorySerializer(history, many=True)
        return Response(serializer.data)


class WatchHistoryDeleteView(APIView):
    def delete(self, request):
        user_id = request.data.get("user_id")
        movie_id = request.data.get("movie_id")

        if not user_id or not movie_id:
            return Response({'error': 'user_id ve movie_id gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            history = WatchHistory.objects.get(user_id=user_id, movie_id=movie_id)
            history.delete()
            return Response({'message': 'İzleme geçmişinden kaldırıldı.'}, status=status.HTTP_200_OK)
        except WatchHistory.DoesNotExist:
            return Response({'error': 'Kayıt bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def recommended_movies(request, user_id):
    # Kullanıcının geçmişi
    favorite_ids = Favorite.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    watched_ids = WatchHistory.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    reviewed_ids = Review.objects.filter(user_id=user_id).values_list('movie_id', flat=True)

    user_movie_ids = set(favorite_ids) | set(watched_ids) | set(reviewed_ids)

    if not user_movie_ids:
        return Response({"error": "Kullanıcının geçmiş verisi bulunamadı."}, status=404)

    # Tüm filmleri al
    all_movies = Movie.objects.prefetch_related('genres').all()
    movie_data = []
    movie_ids = []

    for movie in all_movies:
        genres = " ".join([genre.name for genre in movie.genres.all()])
        combined_text = f"{movie.title} {movie.description} {genres}"
        movie_data.append(combined_text)
        movie_ids.append(movie.id)

    # TF-IDF ile vektörleştir
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(movie_data)

    # Kullanıcının geçmişte izlediği filmlerin indeksleri
    indices_of_user_movies = [movie_ids.index(mid) for mid in user_movie_ids if mid in movie_ids]

    if not indices_of_user_movies:
        return Response({"error": "Kullanıcının geçmişteki filmler TF-IDF vektörlerine eşleşmedi."}, status=400)

    # Ortalama profil vektörü
    user_profile_vector = np.asarray(np.mean(tfidf_matrix[indices_of_user_movies], axis=0))

    # Cosine similarity hesapla
    similarities = cosine_similarity(user_profile_vector, tfidf_matrix).flatten()

    # Önerilecek filmlerin indeksleri (izlemediklerini filtrele)
    recommended_indices = np.argsort(similarities)[::-1]
    recommended_ids = [
                          movie_ids[i] for i in recommended_indices
                          if movie_ids[i] not in user_movie_ids
                      ][:10]  # En fazla 10 öneri

    recommended_movies = Movie.objects.filter(id__in=recommended_ids)
    serializer = MovieSerializer(recommended_movies, many=True)
    return Response(serializer.data)


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


@api_view(["GET"])
def movie_summary(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id).exclude(comment__isnull=True).exclude(comment__exact='')

    if not reviews.exists():
        return Response({"summary": "Bu film hakkında yeterli yorum bulunamadı."}, status=200)

    combined_text = " ".join([review.comment for review in reviews])
    combined_text = combined_text[:1024 * 3]  # BERT/BART gibi modeller için maksimum token sınırı

    try:
        summary = summarizer(combined_text, max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
        return Response({"summary": summary})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
