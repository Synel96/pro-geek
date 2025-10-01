from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from core.models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class BlogPostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'preview_image', 'created_at']

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticated]

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__username', 'sections__title', 'sections__content']
    filterset_fields = ['author', 'created_at']

# Create your views here.
