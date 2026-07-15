from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('series/', views.SeriesListView.as_view(), name='series_list'),
    path('top-rated/', views.TopRatedView.as_view(), name='top_rated'),

    # AJAX views
    path('movie/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('movie/<slug:slug>/rating/', views.add_rating, name='add_rating'),
    path('movie/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('movie/<slug:slug>/download/<int:link_id>/', views.download_movie, name='download_movie'),
]
