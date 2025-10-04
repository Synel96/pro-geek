from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import News
from .serializers import NewsSerializer
from rest_framework.filters import SearchFilter
import sys

class NewsListView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author', 'content']
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
