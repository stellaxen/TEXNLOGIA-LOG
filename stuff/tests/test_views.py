from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class StuffViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.stuff = Stuff.objects.create(username='testuser', phone='1234567890')

    def test_get_stuff_list(self):
        response = self.client.get(reverse('stuff-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'testuser')

    def test_post_stuff(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'phone': '0987654321',
        }
        response = self.client.post(reverse('stuff-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stuff.objects.count(), 2)
