from django.contrib import admin
from django.urls import path
from movies.views import MovieListAPIView, MovieDetailAPIView, FavoriteListCreateView, ReviewListCreateView, \
    ReviewCommentCreateView, ReviewCommentListView, ReviewLikeToggleView, ReviewLikeCountView, ReviewLikeUserListView, \
    UserFavoriteListView, WatchHistoryCreateView, WatchHistoryListView, FavoriteDeleteView, WatchHistoryDeleteView, \
    recommended_movies, movie_summary, MovieCreateAPIView
from users.views import UserCreateAPIView, LoginAPIView, UpdateUserAPIView, CurrentUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Kullanıcı işlemleri
    path('api/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('api/login/', LoginAPIView.as_view(), name='user-login'),
    path('api/update/<int:user_id>/', UpdateUserAPIView.as_view(), name='update-user'),
    path('api/me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('api/movies/create/', MovieCreateAPIView.as_view(), name='movie-create'),

    # Film işlemleri
    path('api/movies/', MovieListAPIView.as_view(), name='movie-list-api'),
    path('api/movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail-api'),
    path('api/recommendations/<int:user_id>/', recommended_movies, name='recommendation-api'),
    path('api/movies/<int:movie_id>/summary/', movie_summary, name='movie-summary'),

    # Favoriler
    path('api/favorites/', FavoriteListCreateView.as_view(), name='favorites'),
    path('api/favorites/user/<int:user_id>/', UserFavoriteListView.as_view(), name='user-favorite-list'),
    path('api/favorites/delete/', FavoriteDeleteView.as_view(), name='favorite-delete'),

    # Yorumlar (Review)
    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),

    # Yorumlara yorum (ReviewComment)
    path('api/reviews/<int:review_id>/comments/', ReviewCommentCreateView.as_view(), name='review-comment-create'),
    path('api/reviews/<int:review_id>/comments/list/', ReviewCommentListView.as_view(), name='review-comment-list'),

    # Beğeni (Like)
    path('api/reviews/<int:review_id>/like/', ReviewLikeToggleView.as_view(), name='review-like-toggle'),
    path('api/reviews/<int:review_id>/likes/count/', ReviewLikeCountView.as_view(), name='review-like-count'),
    path('api/reviews/<int:review_id>/likes/', ReviewLikeUserListView.as_view(), name='review-like-users'),

    # İzleme
    path('api/watch-history/', WatchHistoryCreateView.as_view(), name='watch-history-create'),
    path('api/watch-history/<int:user_id>/', WatchHistoryListView.as_view(), name='watch-history-list'),
    path('api/watch-history/delete/', WatchHistoryDeleteView.as_view(), name='watch-history-delete'),
]
