from rest_framework.serializers import ValidationError


class RelatedHabitOrRewardValidator:
    """Проверяет, что нельзя одновременно заполнить reward и related_habit."""

    def __init__(self, reward_field, related_habit_field):
        self.reward_field = reward_field
        self.related_habit_field = related_habit_field

    def __call__(self, attrs):
        reward = attrs.get(self.reward_field)
        related_habit = attrs.get(self.related_habit_field)
        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )


class ExecutionTimeValidator:
    """Проверяет, что время выполнения не превышает 120 секунд."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        execution_time = attrs.get(self.field)
        if execution_time and execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")


class RelatedHabitIsPleasantValidator:
    """Проверяет, что связанная привычка имеет признак is_pleasant=True."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        related_habit = attrs.get(self.field)
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна быть приятной (is_pleasant=True)."
            )


class PleasantHabitValidator:
    """Проверяет, что у приятной привычки нет reward и related_habit."""

    def __init__(self, is_pleasant_field, reward_field, related_habit_field):
        self.is_pleasant_field = is_pleasant_field
        self.reward_field = reward_field
        self.related_habit_field = related_habit_field

    def __call__(self, attrs):
        is_pleasant = attrs.get(self.is_pleasant_field)
        reward = attrs.get(self.reward_field)
        related_habit = attrs.get(self.related_habit_field)
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class PeriodicityValidator:
    """Проверяет, что периодичность от 1 до 7 дней."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        periodicity = attrs.get(self.field)
        if periodicity and not (1 <= periodicity <= 7):
            raise ValidationError("Периодичность должна быть не более 7 дней.")
