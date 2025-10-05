from rest_framework import serializers
from core.models import News

class NewsSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    def get_preview_image(self, obj):
        if obj.preview_image:
            url = obj.preview_image.url
            return url.replace('/upload/', '/upload/f_auto/')
        return None
    class Meta:
        model = News
        fields = '__all__'
