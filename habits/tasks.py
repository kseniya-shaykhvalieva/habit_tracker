import requests
from celery import shared_task
from django.conf import settings

from habits.models import Habit


@shared_task
def send_habit_reminder():
    """Отправка напоминаний в телеграм для всех привычек"""
    habits = Habit.objects.all()
    for habit in habits:
        user = habit.user
        if user.tg_chat_id:
            message = (
                f"Напоминание: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time}"
            )
            url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
            data = {"chat_id": user.tg_chat_id, "text": message}
            requests.post(url, data=data)
