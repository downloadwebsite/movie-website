from django.contrib import admin
from .models import SiteSettings, FAQ, ContactMessage, Newsletter


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'is_maintenance')

    def has_add_permission(self, request):
        # Only allow one instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description='علامت خوانده شده')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='علامت خوانده نشده')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    list_editable = ('is_active',)
