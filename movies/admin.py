from django.contrib import admin
from .models import (
    Category, Genre, Movie, Series, MovieLink, Comment, Rating, Banner,
    Season, Episode, EpisodeVersion, EpisodeDownloadLink
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'get_movie_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class MovieLinkInline(admin.TabularInline):
    model = MovieLink
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'quality', 'status', 'is_series', 'is_featured',
        'episode_count', 'imdb_rating', 'views_count', 'download_count', 'created_at'
    )
    list_filter = ('status', 'is_featured', 'is_series', 'quality', 'category', 'genres')
    search_fields = ('title', 'description', 'director', 'actors')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category', 'created_by')
    filter_horizontal = ('genres',)
    list_editable = ('status', 'is_featured')
    inlines = [MovieLinkInline, CommentInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'description', 'short_description', 'poster', 'backdrop', 'trailer_url')
        }),
        ('دسته‌بندی و ژانر', {
            'fields': ('category', 'genres')
        }),
        ('اطلاعات فیلم/سریال', {
            'fields': ('release_date', 'duration', 'director', 'actors', 'language', 'country')
        }),
        ('تنظیمات', {
            'fields': ('quality', 'status', 'is_featured', 'is_series', 'episode_count')
        }),
        ('آمار', {
            'fields': ('imdb_rating', 'views_count', 'download_count')
        }),
        ('سازنده', {
            'fields': ('created_by',)
        }),
    )

    actions = ['make_series', 'make_movie', 'publish_selected', 'archive_selected']

    @admin.action(description='تبدیل به سریال')
    def make_series(self, request, queryset):
        updated = queryset.update(is_series=True)
        self.message_user(request, f'{updated} مورد به سریال تبدیل شد.')

    @admin.action(description='تبدیل به فیلم')
    def make_movie(self, request, queryset):
        updated = queryset.update(is_series=False)
        self.message_user(request, f'{updated} مورد به فیلم تبدیل شد.')

    @admin.action(description='انتشار انتخاب شده')
    def publish_selected(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} مورد منتشر شد.')

    @admin.action(description='بایگانی انتخاب شده')
    def archive_selected(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} مورد بایگانی شد.')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'quality', 'status', 'is_featured',
        'episode_count', 'imdb_rating', 'views_count', 'download_count', 'created_at'
    )
    list_filter = ('status', 'is_featured', 'quality', 'category', 'genres')
    search_fields = ('title', 'description', 'director', 'actors')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category', 'created_by')
    filter_horizontal = ('genres',)
    list_editable = ('status', 'is_featured', 'episode_count')
    inlines = [MovieLinkInline, CommentInline]

    fieldsets = (
        ('اطلاعات اصلی سریال', {
            'fields': ('title', 'slug', 'description', 'short_description', 'poster', 'backdrop', 'trailer_url')
        }),
        ('دسته‌بندی و ژانر', {
            'fields': ('category', 'genres')
        }),
        ('اطلاعات سریال', {
            'fields': ('release_date', 'director', 'actors', 'language', 'country')
        }),
        ('تنظیمات سریال', {
            'fields': ('quality', 'status', 'is_featured', 'episode_count')
        }),
        ('آمار', {
            'fields': ('imdb_rating', 'views_count', 'download_count')
        }),
        ('سازنده', {
            'fields': ('created_by',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_series=True)

    def save_model(self, request, obj, form, change):
        obj.is_series = True
        super().save_model(request, obj, form, change)

    actions = ['publish_series', 'archive_series', 'convert_to_movie']

    @admin.action(description='انتشار سریال‌های انتخاب شده')
    def publish_series(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} سریال منتشر شد.')

    @admin.action(description='بایگانی سریال‌های انتخاب شده')
    def archive_series(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} سریال بایگانی شد.')

    @admin.action(description='تبدیل به فیلم')
    def convert_to_movie(self, request, queryset):
        updated = queryset.update(is_series=False)
        self.message_user(request, f'{updated} سریال به فیلم تبدیل شد.')


# ===== Inline Admin for Series Structure =====

class EpisodeDownloadLinkInline(admin.TabularInline):
    model = EpisodeDownloadLink
    extra = 0
    fields = ('quality', 'url', 'file_size', 'download_count', 'is_active')
    readonly_fields = ('download_count',)


class EpisodeVersionInline(admin.StackedInline):
    model = EpisodeVersion
    extra = 1
    fields = ('version_type', 'title', 'language', 'has_subtitle')
    inlines = [EpisodeDownloadLinkInline]


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1
    fields = ('number', 'title', 'description', 'duration', 'release_date', 'views_count')
    readonly_fields = ('views_count',)
    show_change_link = True


class SeasonInline(admin.StackedInline):
    model = Season
    extra = 1
    fields = ('number', 'title', 'description', 'release_year', 'episode_count')
    inlines = [EpisodeInline]
    show_change_link = True


# ===== Register Season Admin =====

class EpisodeVersionInlineForSeason(admin.TabularInline):
    model = EpisodeVersion
    extra = 0
    fields = ('episode', 'version_type', 'title', 'language', 'has_subtitle')
    readonly_fields = ()


class EpisodeDownloadLinkInlineForSeason(admin.TabularInline):
    model = EpisodeDownloadLink
    extra = 0
    fields = ('quality', 'url', 'file_size', 'download_count', 'is_active')
    readonly_fields = ('download_count',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'get_title_display', 'number', 'release_year', 'episode_count', 'created_at')
    list_filter = ('series', 'release_year')
    search_fields = ('series__title', 'title', 'description')
    raw_id_fields = ('series',)
    list_editable = ('episode_count',)
    inlines = [EpisodeInline]

    def get_title_display(self, obj):
        return obj.get_title_display()
    get_title_display.short_description = 'عنوان فصل'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('series')

    actions = ['update_episode_count']

    @admin.action(description='بروزرسانی تعداد قسمت‌ها')
    def update_episode_count(self, request, queryset):
        for season in queryset:
            season.episode_count = season.episodes.count()
            season.save(update_fields=['episode_count'])
        self.message_user(request, 'تعداد قسمت‌ها بروزرسانی شد.')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'series_title', 'season_number', 'number', 'title', 'duration',
        'release_date', 'views_count', 'created_at'
    )
    list_filter = ('season__series', 'season', 'release_date')
    search_fields = ('season__series__title', 'title', 'description')
    raw_id_fields = ('season',)
    readonly_fields = ('views_count',)
    list_editable = ('duration',)
    inlines = [EpisodeVersionInline]

    def series_title(self, obj):
        return obj.season.series.title
    series_title.short_description = 'سریال'

    def season_number(self, obj):
        return obj.season.get_title_display()
    season_number.short_description = 'فصل'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('season', 'season__series')


@admin.register(EpisodeVersion)
class EpisodeVersionAdmin(admin.ModelAdmin):
    list_display = (
        'series_title', 'season_number', 'episode_number', 'get_version_type_display',
        'language', 'has_subtitle', 'download_links_count', 'created_at'
    )
    list_filter = ('version_type', 'language', 'has_subtitle')
    search_fields = ('episode__season__series__title', 'title')
    raw_id_fields = ('episode',)
    list_editable = ('has_subtitle',)
    inlines = [EpisodeDownloadLinkInline]

    def series_title(self, obj):
        return obj.episode.season.series.title
    series_title.short_description = 'سریال'

    def season_number(self, obj):
        return obj.episode.season.get_title_display()
    season_number.short_description = 'فصل'

    def episode_number(self, obj):
        return f'قسمت {obj.episode.number}'
    episode_number.short_description = 'قسمت'

    def get_version_type_display(self, obj):
        return obj.get_version_type_display()
    get_version_type_display.short_description = 'نوع نسخه'

    def download_links_count(self, obj):
        return obj.download_links.count()
    download_links_count.short_description = 'تعداد لینک‌ها'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('episode', 'episode__season', 'episode__series')


@admin.register(EpisodeDownloadLink)
class EpisodeDownloadLinkAdmin(admin.ModelAdmin):
    list_display = (
        'series_title', 'season_number', 'episode_number', 'version_type',
        'quality', 'file_size', 'download_count', 'is_active'
    )
    list_filter = ('quality', 'is_active', 'version__version_type')
    search_fields = ('version__episode__season__series__title', 'url')
    raw_id_fields = ('version',)
    list_editable = ('is_active',)
    readonly_fields = ('download_count',)

    def series_title(self, obj):
        return obj.version.episode.season.series.title
    series_title.short_description = 'سریال'

    def season_number(self, obj):
        return obj.version.episode.season.get_title_display()
    season_number.short_description = 'فصل'

    def episode_number(self, obj):
        return f'قسمت {obj.version.episode.number}'
    episode_number.short_description = 'قسمت'

    def version_type(self, obj):
        return obj.version.get_version_type_display()
    version_type.short_description = 'نوع نسخه'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'version', 'version__episode', 'version__episode__season', 'version__episode__series'
        )


@admin.register(MovieLink)
class MovieLinkAdmin(admin.ModelAdmin):
    list_display = ('movie', 'quality', 'link_type', 'file_size', 'subtitle', 'is_active', 'download_count')
    list_filter = ('quality', 'link_type', 'is_active', 'subtitle')
    search_fields = ('movie__title', 'url')
    raw_id_fields = ('movie',)
    list_editable = ('is_active',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'text', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'movie__title', 'text')
    raw_id_fields = ('user', 'movie', 'parent')
    list_editable = ('is_approved',)
    actions = ['approve_comments', 'reject_comments']

    @admin.action(description='تایید نظرات انتخاب شده')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='رد نظرات انتخاب شده')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user__username', 'movie__title')
    raw_id_fields = ('user', 'movie')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    raw_id_fields = ('movie',)
    list_editable = ('is_active', 'order')


# Custom Admin Site Configuration
admin.site.site_header = 'مدیریت فیلم و سریال'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'خوش آمدید'
