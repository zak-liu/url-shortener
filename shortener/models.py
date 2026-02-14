from django.db import models
from django.contrib.auth.models import User

class ShortenedURL(models.Model):
    # Original long URL
    original_url = models.URLField(max_length=500)
    # Unique code for shortening
    short_code = models.CharField(max_length=15, unique=True)
    # Correct parameter is "on_delete"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class ClickDetail(models.Model):
    # Link to the shortened URL record
    url_record = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    # Capture source IP
    ip_address = models.GenericIPAddressField()
    # Capture user device info
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Click on {self.url_record.short_code} from {self.ip_address}"