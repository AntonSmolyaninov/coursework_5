from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_execution_time(value):
    if value > 120:
        raise ValidationError(_("Время выполнения не должно превышать 120 секунд"))


def validate_periodicity(value):
    if value > 7:
        raise ValidationError(_("Периодичность не должна превышать 7 дней"))
