from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserFavorite, DownloadHistory


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_active', 'is_staff', 'email_verified')
    list_filter = ('is_active', 'is_staff', 'email_verified')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {'fields': ('avatar', 'phone', 'birth_date', 'bio', 'email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {'fields': ('avatar', 'phone', 'birth_date', 'bio')}),
    )


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'movie__title')
    raw_id_fields = ('user', 'movie')


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'quality', 'downloaded_at')
    list_filter = ('quality', 'downloaded_at')
    search_fields = ('user__username', 'movie__title')
    raw_id_fields = ('user', 'movie')
