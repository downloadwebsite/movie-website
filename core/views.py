from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db import connection
from .models import SiteSettings, FAQ, ContactMessage, Newsletter
from django.contrib import messages


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'ok', 'database': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context


class FAQView(TemplateView):
    template_name = 'core/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context


class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')

        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
        else:
            messages.error(request, 'لطفا تمام فیلدها را پر کنید.')

        return render(request, self.template_name, self.get_context_data(**kwargs))


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                messages.success(request, 'شما با موفقیت در خبرنامه عضو شدید.')
            else:
                messages.info(request, 'شما قبلا در خبرنامه عضو شده‌اید.')
        else:
            messages.error(request, 'لطفا ایمیل خود را وارد کنید.')

    return render(request, 'core/newsletter.html')
