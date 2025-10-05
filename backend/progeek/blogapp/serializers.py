from rest_framework import serializers
from core.models import BlogPost, BlogSection, SectionImage, SectionVideo

class SectionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        if obj.image:
            url = obj.image.url
            return url.replace('/upload/', '/upload/f_auto/')
        return None
    class Meta:
        model = SectionImage
        fields = ['id', 'image']

class SectionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionVideo
        fields = ['id', 'video']

class BlogSectionSerializer(serializers.ModelSerializer):
    images = SectionImageSerializer(many=True, read_only=True)
    videos = SectionVideoSerializer(many=True, read_only=True)
    class Meta:
        model = BlogSection
        fields = ['id', 'title', 'content', 'images', 'videos']

class BlogPostSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()
    sections = BlogSectionSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    def get_preview_image(self, obj):
        if obj.preview_image:
            url = obj.preview_image.url
            return url.replace('/upload/', '/upload/f_auto/')
        return None
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'preview_image', 'created_at', 'updated_at', 'sections']
