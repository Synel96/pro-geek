from rest_framework import serializers
from core.models import News

class NewsSerializer(serializers.ModelSerializer):
    preview_image = serializers.ImageField(use_url=True)
    class Meta:
        model = News
        fields = '__all__'
