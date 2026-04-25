from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "time", "place", "is_pleasant", "is_public")
    list_filter = ("is_pleasant", "is_public", "periodicity")
    search_fields = ("action", "user__username")
