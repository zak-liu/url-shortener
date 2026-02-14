from rest_framework import serializers
from .models import ShortenedURL # 假設你的 model 名稱

class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['id', 'original_url', 'short_code', 'created_at']
        read_only_fields = ['short_code', 'created_at']