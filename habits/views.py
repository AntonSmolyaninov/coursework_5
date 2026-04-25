from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Habit
from .pagination import HabitPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitPublicSerializer, HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(models.Q(user=self.request.user) | models.Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my(self, request):
        habits = Habit.objects.filter(user=request.user)
        page = self.paginate_queryset(habits)
        if page:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(habits, many=True).data)

    @action(detail=False, methods=["get"])
    def public(self, request):
        habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(habits)
        if page:
            return self.get_paginated_response(HabitPublicSerializer(page, many=True).data)
        return Response(HabitPublicSerializer(habits, many=True).data)
