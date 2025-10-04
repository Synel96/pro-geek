from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import Event
from .serializers import EventSerializer
from django.views.decorators.cache import cache_page
from rest_framework.filters import SearchFilter
import sys

class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['event_title', 'host', 'event_type', 'location']
    if not ('test' in sys.argv or 'pytest' in sys.argv):
        @cache_page(60 * 15)
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
    else:
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
