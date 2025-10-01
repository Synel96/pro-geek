from rest_framework import serializers
from core.models import BlogPost, BlogSection, SectionImage, SectionVideo

class SectionImageSerializer(serializers.ModelSerializer):
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
    sections = BlogSectionSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'preview_image', 'created_at', 'updated_at', 'sections']
