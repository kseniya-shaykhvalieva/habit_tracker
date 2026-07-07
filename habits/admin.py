from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "user",)
    list_filter = ("user",)
    search_fields = ("action",)
