from django.db import models

from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """Привычка"""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="Связанная привычка")
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (дни)")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveSmallIntegerField(verbose_name="Время на выполнение (сек)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
