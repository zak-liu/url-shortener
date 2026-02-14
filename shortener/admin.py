# Register your models here.
from django.contrib import admin
from .models import ShortenedURL, ClickDetail

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'created_at')

# Register ClickDetail with a custom admin interface to show relevant information
@admin.register(ClickDetail)
class ClickDetailAdmin(admin.ModelAdmin):
    list_display = ('url_record', 'ip_address', 'clicked_at')