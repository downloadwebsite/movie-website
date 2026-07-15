from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from .models import User, DownloadHistory, UserFavorite
from movies.models import Movie


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['download_history'] = DownloadHistory.objects.filter(
            user=user
        ).select_related('movie')[:10]
        context['favorites'] = UserFavorite.objects.filter(
            user=user
        ).select_related('movie')[:12]
        context['total_downloads'] = DownloadHistory.objects.filter(user=user).count()
        context['total_favorites'] = UserFavorite.objects.filter(user=user).count()
        return context


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = UserFavorite.objects.filter(
            user=self.request.user
        ).select_related('movie')
        return context


class DownloadHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/download_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = DownloadHistory.objects.filter(
            user=self.request.user
        ).select_related('movie')
        return context


def register_view(request):
    if request.user.is_authenticated:
        return redirect('movies:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت نام با موفقیت انجام شد.')
            return redirect('movies:home')
        else:
            messages.error(request, 'لطفا اطلاعات را صحیح وارد کنید.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movies:home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود موفقیت‌آمیز بود.')
                next_url = request.GET.get('next', 'movies:home')
                return redirect(next_url)
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید.')
    return redirect('movies:home')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'لطفا اطلاعات را صحیح وارد کنید.')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})
