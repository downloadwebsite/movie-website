from django.urls import path, re_path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    re_path(r'^movie/(?P<slug>[\w\u0600-\u06FF-]+)/$', views.MovieDetailView.as_view(), name='movie_detail'),
    re_path(r'^category/(?P<slug>[\w\u0600-\u06FF-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('series/', views.SeriesListView.as_view(), name='series_list'),
    path('top-rated/', views.TopRatedView.as_view(), name='top_rated'),

    # AJAX views
    re_path(r'^movie/(?P<slug>[\w\u0600-\u06FF-]+)/comment/$', views.add_comment, name='add_comment'),
    re_path(r'^movie/(?P<slug>[\w\u0600-\u06FF-]+)/rating/$', views.add_rating, name='add_rating'),
    re_path(r'^movie/(?P<slug>[\w\u0600-\u06FF-]+)/favorite/$', views.toggle_favorite, name='toggle_favorite'),
    re_path(r'^movie/(?P<slug>[\w\u0600-\u06FF-]+)/download/(?P<link_id>\d+)/$', views.download_movie, name='download_movie'),
]
