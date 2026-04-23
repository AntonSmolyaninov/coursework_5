# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')  # Добавьте basename

urlpatterns = [
    path('', include(router.urls)),
]
