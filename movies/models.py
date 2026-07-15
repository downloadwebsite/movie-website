from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movies:category_detail', kwargs={'slug': self.slug})

    def get_movie_count(self):
        return self.movies.filter(status='published').count()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانرها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Movie(models.Model):
    QUALITY_CHOICES = [
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('2160p', '4K'),
    ]

    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'بایگانی شده'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True)
    backdrop = models.ImageField(upload_to='movies/backdrops/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, help_text='YouTube trailer URL')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='movies')
    genres = models.ManyToManyField(Genre, blank=True, related_name='movies')

    release_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text='مدت زمان به دقیقه', blank=True, null=True)
    director = models.CharField(max_length=200, blank=True)
    actors = models.CharField(max_length=500, blank=True, help_text='نام بازیگران با کاما جدا شده')
    language = models.CharField(max_length=50, default='فارسی (دوبله)')
    country = models.CharField(max_length=100, blank=True)

    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='1080p')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_series = models.BooleanField(default=False, help_text='آیا این فیلم سریال است؟')
    episode_count = models.PositiveIntegerField(default=1, help_text='تعداد قسمت‌ها')

    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_movies')

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movies:movie_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_downloads(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def get_genres_list(self):
        return list(self.genres.values_list('name', flat=True))

    def get_poster_url(self):
        if self.poster and hasattr(self.poster, 'url'):
            return self.poster.url
        return '/static/images/no-poster.jpg'

    def get_backdrop_url(self):
        if self.backdrop and hasattr(self.backdrop, 'url'):
            return self.backdrop.url
        return self.get_poster_url()


class MovieLink(models.Model):
    QUALITY_CHOICES = [
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('2160p', '4K'),
    ]

    LINK_TYPE_CHOICES = [
        ('direct', 'لینک مستقیم'),
        ('torrent', 'تورنت'),
        ('online', 'پخش آنلاین'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='links')
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    link_type = models.CharField(max_length=10, choices=LINK_TYPE_CHOICES, default='direct')
    url = models.URLField()
    file_size = models.CharField(max_length=20, blank=True, help_text='مثال: 1.5GB')
    subtitle = models.BooleanField(default=False, help_text='آیا زیرنویس دارد؟')
    language = models.CharField(max_length=50, default='فارسی (دوبله)')
    is_active = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'لینک دانلود'
        verbose_name_plural = 'لینک‌های دانلود'
        ordering = ['quality']

    def __str__(self):
        return f'{self.movie.title} - {self.quality}'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

    def get_replies(self):
        return self.replies.filter(is_approved=True)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveIntegerField(help_text='امتیاز از 1 تا 10')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
        unique_together = ('movie', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}: {self.score}'

    def save(self, *args, **kwargs):
        if self.score < 1 or self.score > 10:
            raise ValueError('امتیاز باید بین 1 تا 10 باشد')
        super().save(*args, **kwargs)


class Banner(models.Model):
    title = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
        ordering = ['order']

    def __str__(self):
        return self.title


class SeriesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_series=True)


class Series(Movie):
    objects = SeriesManager()

    class Meta:
        proxy = True
        verbose_name = 'سریال'
        verbose_name_plural = 'سریال‌ها'

    def save(self, *args, **kwargs):
        self.is_series = True
        super().save(*args, **kwargs)


# ===== Models for Series Structure =====

class Season(models.Model):
    """فصل سریال"""
    series = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons', verbose_name='سریال')
    number = models.PositiveIntegerField(verbose_name='شماره فصل')
    title = models.CharField(max_length=200, blank=True, verbose_name='عنوان فصل', help_text='مثال: فصل اول')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    release_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='سال انتشار')
    episode_count = models.PositiveIntegerField(default=0, verbose_name='تعداد قسمت‌ها')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل‌ها'
        ordering = ['number']
        unique_together = ('series', 'number')

    def __str__(self):
        return f'{self.series.title} - {self.get_title_display()}'

    def get_title_display(self):
        if self.title:
            return self.title
        persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم', 'ششم', 'هفتم', 'هشتم', 'نهم', 'دهم']
        if self.number <= len(persian_numbers):
            return f'فصل {persian_numbers[self.number - 1]}'
        return f'فصل {self.number}'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_title_display()
        super().save(*args, **kwargs)


class Episode(models.Model):
    """قسمت سریال"""
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes', verbose_name='فصل')
    number = models.PositiveIntegerField(verbose_name='شماره قسمت')
    title = models.CharField(max_length=200, blank=True, verbose_name='عنوان قسمت')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    duration = models.PositiveIntegerField(blank=True, null=True, verbose_name='مدت زمان (دقیقه)')
    release_date = models.DateField(blank=True, null=True, verbose_name='تاریخ انتشار')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'قسمت'
        verbose_name_plural = 'قسمت‌ها'
        ordering = ['number']
        unique_together = ('season', 'number')

    def __str__(self):
        return f'{self.season.series.title} - {self.season.get_title_display()} - قسمت {self.number}'

    def get_absolute_url(self):
        return reverse('movies:episode_detail', kwargs={
            'series_slug': self.season.series.slug,
            'season_number': self.season.number,
            'episode_number': self.number
        })


class EpisodeVersion(models.Model):
    """نسخه قسمت (زیرنویس یا دوبله)"""
    VERSION_TYPE_CHOICES = [
        ('subtitle', 'زیرنویس فارسی'),
        ('dubbed', 'دوبله فارسی'),
        ('original', 'زبان اصلی'),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='versions', verbose_name='قسمت')
    version_type = models.CharField(max_length=10, choices=VERSION_TYPE_CHOICES, verbose_name='نوع نسخه')
    title = models.CharField(max_length=200, blank=True, verbose_name='عنوان نسخه')
    language = models.CharField(max_length=50, default='فارسی', verbose_name='زبان')
    has_subtitle = models.BooleanField(default=False, verbose_name='زیرنویس فارسی')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'نسخه قسمت'
        verbose_name_plural = 'نسخه‌های قسمت'
        ordering = ['version_type']
        unique_together = ('episode', 'version_type')

    def __str__(self):
        return f'{self.episode} - {self.get_version_type_display()}'

    def get_version_type_display(self):
        return dict(self.VERSION_TYPE_CHOICES).get(self.version_type, self.version_type)

    def get_title_display(self):
        if self.title:
            return self.title
        return self.get_version_type_display()


class EpisodeDownloadLink(models.Model):
    """لینک دانلود قسمت"""
    QUALITY_CHOICES = [
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('2160p', '4K'),
    ]

    version = models.ForeignKey(EpisodeVersion, on_delete=models.CASCADE, related_name='download_links', verbose_name='نسخه')
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, verbose_name='کیفیت')
    url = models.URLField(verbose_name='لینک دانلود')
    file_size = models.CharField(max_length=20, blank=True, verbose_name='حجم فایل', help_text='مثال: 350MB')
    download_count = models.PositiveIntegerField(default=0, verbose_name='تعداد دانلود')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'لینک دانلود قسمت'
        verbose_name_plural = 'لینک‌های دانلود قسمت'
        ordering = ['quality']
        unique_together = ('version', 'quality')

    def __str__(self):
        return f'{self.version} - {self.quality}'

    def increment_downloads(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])
