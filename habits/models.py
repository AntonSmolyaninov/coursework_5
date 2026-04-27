from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .validators import validate_execution_time, validate_periodicity


class Habit(models.Model):
    class Periodicity(models.IntegerChoices):
        DAILY = 1, "Ежедневно"
        EVERY_TWO_DAYS = 2, "Каждые 2 дня"
        EVERY_THREE_DAYS = 3, "Каждые 3 дня"
        WEEKLY = 7, "Еженедельно"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.IntegerField(
        choices=Periodicity.choices, default=Periodicity.DAILY, validators=[validate_periodicity]
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(
        validators=[validate_execution_time], verbose_name="Время выполнения (сек)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reminded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать и вознаграждение, и связанную привычку")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def should_remind_today(self):
        if not self.last_reminded_at:
            return True
        days_since = (timezone.now().date() - self.last_reminded_at.date()).days
        return days_since >= self.periodicity
