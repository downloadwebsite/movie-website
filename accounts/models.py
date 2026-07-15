from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'


class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='download_history')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='download_history')
    quality = models.CharField(max_length=20)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تاریخچه دانلود'
        verbose_name_plural = 'تاریخچه دانلودها'
        ordering = ['-downloaded_at']

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} ({self.quality})'
