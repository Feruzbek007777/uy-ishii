from django.urls import path
from .views import (
    about, MovieCreateView, delete_movie, update_movie,
    GenreView, MovieDetailDetail, ProfileView, logout_view, HomeView
)

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('about/', about, name='about'),
    path('movie/add/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:movie_id>/delete/', delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/update/', update_movie, name='update_movie'),
    path('genre/<int:genre_id>/', GenreView.as_view(), name='by_genre'),
    path('movie/<int:movie_id>/', MovieDetailDetail.as_view(), name='by_movie'),
    path('profile/<str:username>/', ProfileView.as_view(), name="profile"),
    path('logout/', logout_view, name='logout'),
]
