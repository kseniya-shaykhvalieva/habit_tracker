from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validations import (ExecutionTimeValidator, PeriodicityValidator,
                                PleasantHabitValidator,
                                RelatedHabitIsPleasantValidator,
                                RelatedHabitOrRewardValidator)


class HabitSerializer(ModelSerializer):
    """Сериализатор для привычек с подключёнными валидаторами."""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitOrRewardValidator("reward", "related_habit"),
            ExecutionTimeValidator("execution_time"),
            RelatedHabitIsPleasantValidator("related_habit"),
            PleasantHabitValidator("is_pleasant", "reward", "related_habit"),
            PeriodicityValidator("periodicity"),
        ]
