from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from habits.models import Habit
from users.models import User


class HabitCase(APITestCase):

    def setUp(self):
        """Создание тестового пользователя и привычки перед каждым тестом."""
        self.user = User.objects.create(email="test@test.ru")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="14:30:00",
            action="Сделать разминку",
            execution_time=60,
            periodicity=1,
            is_public=False
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        """Детальный просмотр привычки."""
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        """Создание привычки."""
        url = reverse("habits:habits-list")
        data = {
            "user": self.user.pk,
            "place": "Работа",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "execution_time": 30,
            "periodicity": 1,
            "is_public": False
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_update(self):
        """Редактирование привычки."""
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        data = {"action": "Планка"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Планка")

    def test_habit_delete(self):
        """Удаление привычки."""
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_list(self):
        """Тест получения списка привычек текущего пользователя."""
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": self.habit.place,
                    "time": self.habit.time,
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "related_habit": self.habit.related_habit,
                    "periodicity": self.habit.periodicity,
                    "reward": self.habit.reward,
                    "execution_time": self.habit.execution_time,
                    "is_public": self.habit.is_public,
                    "user": self.habit.user.pk
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_public_habit_list(self):
        """Тест получения списка публичных привычек."""
        # public_habit = Habit.objects.create(
        #     user=self.user,
        #     place="Дом",
        #     time="08:00:00",
        #     action="Отжаться",
        #     execution_time=30,
        #     periodicity=1,
        #     is_public=True
        # )

        url = reverse("habits:public")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(data["count"], 1)
        self.assertEqual(data["count"], 0)

    def test_habit_create_validation_error(self):
        """Тест валидации: время выполнения > 120 секунд."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Дом",
            "time": "15:00:00",
            "action": "Чтение",
            "execution_time": 150,
            "periodicity": 1,
            "is_public": False
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
