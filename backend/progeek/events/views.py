from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import Event
from .serializers import EventSerializer
from django.views.decorators.cache import cache_page

class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    @cache_page(60 * 15)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
