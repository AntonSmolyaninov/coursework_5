import logging

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(chat_id, message):
    if not settings.TELEGRAM_BOT_TOKEN:
        return {"error": "Bot token not configured"}

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return {"error": str(e)}


@shared_task
def check_and_send_reminders():
    from .models import Habit

    now = timezone.now()
    habits = Habit.objects.filter(is_pleasant=False, user__telegram_chat_id__isnull=False)

    for habit in habits:
        if habit.time.hour == now.hour and habit.time.minute == now.minute and habit.should_remind_today():
            message = f"<b>Напоминание!</b>\n\n{habit.action}\n {habit.place}\n {habit.time.strftime('%H:%M')}"
            if habit.reward:
                message += f"\nВознаграждение: {habit.reward}"
            send_telegram_message.delay(habit.user.telegram_chat_id, message)
            habit.last_reminded_at = now
            habit.save(update_fields=["last_reminded_at"])
