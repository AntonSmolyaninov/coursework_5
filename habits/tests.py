from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_create_valid_habit(self):
        habit = Habit.objects.create(
            user=self.user, place='Home', time='08:00:00', action='Exercise',
            execution_time=60, reward='Reward'
        )
        self.assertEqual(habit.action, 'Exercise')

    def test_execution_time_exceeds_limit(self):
        with self.assertRaises(ValidationError):
            Habit.objects.create(
                user=self.user, place='Home', time='08:00:00', action='Exercise',
                execution_time=150, reward='Reward'
            )

    def test_periodicity_limit(self):
        with self.assertRaises(ValidationError):
            Habit.objects.create(
                user=self.user, place='Home', time='08:00:00', action='Exercise',
                execution_time=60, periodicity=14, reward='Reward'
            )


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse('habit-list')
        data = {'place': 'Home', 'time': '08:00:00', 'action': 'Run', 'execution_time': 60, 'reward': 'Smoothie'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        Habit.objects.create(user=self.user, place='Home', time='08:00:00', action='Exercise', execution_time=60, reward='Reward')
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_habits_endpoint(self):
        Habit.objects.create(user=self.user, place='Home', time='08:00:00', action='My habit', execution_time=60, reward='Reward')
        url = reverse('habit-my')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_habits_endpoint(self):
        Habit.objects.create(user=self.user, place='Park', time='10:00:00', action='Public habit', execution_time=45, is_public=True, reward='Fresh air')
        url = reverse('habit-public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAuthTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'StrongPass123!', 'email': 'new@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
