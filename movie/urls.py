from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . views import *


urlpatterns = [
    path('', MovieBanner.as_view(), name="home"),
    path('signup/', UserRegister.as_view(), name="signup"),
    path('update/', UserUpdate.as_view(), name="user_update"),
    path('password/update/', PasswordUpdate.as_view(), name="password_update"),
    path('login/', MyLoginView.as_view(template_name="movie/home.html"), name="login"),
    path('movies/', Movies.as_view(), name="movies"),
    path('movie/<int:pk>/', Movie.as_view(), name="movie"),
    path('celebrity/<slug:slug>/', Celebrity.as_view(), name="celebrity"),
    path('category/<str:category>/', MovieCategory.as_view(), name="movie_category"),
    path('status/<str:status>/', MovieStatus.as_view(), name="movie_status"),
    path('language/<str:language>/', MovieLanguage.as_view(), name="movie_language"),
    path('blog/<slug:slug>/', Blog.as_view(), name="blog"),
    path('comment/<slug:slug>/', NewsComment.as_view(), name="comments"),
    path('search/', MovieSearch.as_view(), name="movie-search"),
    path('logout/', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path('series/', series, name="series"),
    path('celebrity/', Celebritys.as_view(), name="celebrity"),
    path('blogs/', Blogs.as_view(), name="blogs"),
    path('favorites/', Favorite.as_view(), name="favorites"),
    path('favorite/<slug:slug>/', add_to_favorites, name="add_to_favorites"),
    path('profile/', Profile.as_view(), name="profile"),
    path('profile/pic/update/', Profile_pic_update.as_view(), name="pic_update"),
    path('rate/', rate, name="rate"),
    path('error/', error, name="error"),
    path('comingsoon/', comingsoon, name="comingsoon"),
]
