from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('download-history/', views.DownloadHistoryView.as_view(), name='download_history'),
]
