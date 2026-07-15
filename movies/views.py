from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    Movie, Category, Genre, Comment, Rating, Banner, MovieLink
)
from accounts.models import UserFavorite, DownloadHistory
from core.models import SiteSettings


class HomeView(TemplateView):
    template_name = 'movies/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_movies'] = Movie.objects.filter(
            is_featured=True, status='published'
        )[:6]
        context['latest_movies'] = Movie.objects.filter(
            status='published'
        )[:12]
        context['series_movies'] = Movie.objects.filter(
            is_series=True, status='published'
        )[:6]
        context['categories'] = Category.objects.filter(is_active=True)[:8]
        context['banners'] = Banner.objects.filter(is_active=True)[:5]
        context['top_rated'] = Movie.objects.filter(
            status='published'
        ).annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')[:6]
        context['most_viewed'] = Movie.objects.filter(
            status='published'
        ).order_by('-views_count')[:6]
        context['most_downloaded'] = Movie.objects.filter(
            status='published'
        ).order_by('-download_count')[:6]
        return context


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.filter(status='published')
        category_slug = self.kwargs.get('category_slug')
        genre_slug = self.kwargs.get('genre_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            queryset = queryset.filter(genres=genre)

        # Sorting
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'most_viewed':
            queryset = queryset.order_by('-views_count')
        elif sort == 'most_downloaded':
            queryset = queryset.order_by('-download_count')
        elif sort == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('ratings__score')
            ).order_by('-avg_rating')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['genres'] = Genre.objects.all()
        context['current_category'] = self.kwargs.get('category_slug')
        context['current_genre'] = self.kwargs.get('genre_slug')
        context['sort'] = self.request.GET.get('sort', 'newest')
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object
        context['comments'] = movie.comments.filter(
            is_approved=True, parent=None
        ).select_related('user')
        context['links'] = movie.links.filter(is_active=True)
        context['related_movies'] = Movie.objects.filter(
            category=movie.category,
            status='published'
        ).exclude(id=movie.id)[:6]
        context['avg_rating'] = movie.ratings.aggregate(
            avg=Avg('score')
        )['avg']
        context['rating_count'] = movie.ratings.count()

        if self.request.user.is_authenticated:
            context['user_rating'] = Rating.objects.filter(
                movie=movie, user=self.request.user
            ).first()
            context['is_favorite'] = UserFavorite.objects.filter(
                movie=movie, user=self.request.user
            ).exists()

        return context


class CategoryDetailView(ListView):
    template_name = 'movies/category_detail.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Movie.objects.filter(
            category=self.category, status='published'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class SearchView(ListView):
    template_name = 'movies/search.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Movie.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(director__icontains=query) |
                Q(actors__icontains=query),
                status='published'
            ).distinct()
        return Movie.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class SeriesListView(ListView):
    template_name = 'movies/series_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        return Movie.objects.filter(
            is_series=True, status='published'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class TopRatedView(ListView):
    template_name = 'movies/top_rated.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        return Movie.objects.filter(
            status='published'
        ).annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


# API Views
@login_required
def add_comment(request, slug):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, slug=slug)
        text = request.POST.get('text', '')
        parent_id = request.POST.get('parent_id')

        if text:
            comment = Comment.objects.create(
                movie=movie,
                user=request.user,
                text=text,
                parent_id=parent_id if parent_id else None
            )
            messages.success(request, 'نظر شما با موفقیت اضافه شد.')
        else:
            messages.error(request, 'لطفا متن نظر را وارد کنید.')

    return redirect('movies:movie_detail', slug=slug)


@login_required
def add_rating(request, slug):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, slug=slug)
        score = request.POST.get('score')

        if score:
            rating, created = Rating.objects.update_or_create(
                movie=movie,
                user=request.user,
                defaults={'score': int(score)}
            )
            messages.success(request, 'امتیاز شما ثبت شد.')

    return redirect('movies:movie_detail', slug=slug)


@login_required
def toggle_favorite(request, slug):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, slug=slug)
        favorite, created = UserFavorite.objects.get_or_create(
            movie=movie,
            user=request.user
        )

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed'})

        return JsonResponse({'status': 'added'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def download_movie(request, slug, link_id):
    movie = get_object_or_404(Movie, slug=slug)
    link = get_object_or_404(MovieLink, id=link_id, movie=movie, is_active=True)

    # Record download
    DownloadHistory.objects.create(
        user=request.user,
        movie=movie,
        quality=link.quality
    )

    # Increment counters
    movie.increment_downloads()
    link.download_count += 1
    link.save(update_fields=['download_count'])

    return redirect(link.url)
