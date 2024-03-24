from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *
from .serializers import *
from .views import *


class PerevalTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'email': 'test@example.com',
            'fam': '1',
            'name': 'test',
            'otc': '1',
            'phone': '1234567890',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['email'], data['email'])


    def test_create_pereval(self):
        factory_1 = APIRequestFactory()
        request_1 = factory_1.post('/api/pereval/', {
            'email': '<EMAIL>',
            'fam': '1',
            'name': 'test',
            'otc': '1',
            'phone': '1234567890',
            'coords': {
                'latitude': 123,
                'longitude': 123,
                'height': 123
            },
            'level': {
                'winter': '1',
                'summer': '1',
                'autumn': '1',
                'spring': '1',
            },
            'images': [
                {
                    'data': 'test',
                    'title': 'test'
                }
            ]
        }, format='json')
        response_1 = PerevalViewset.as_view({'post': 'create'})(request_1)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)

    def test_partial_update_pereval(self):
        self.user = User.objects.create(
            email='<EMAIL>',
            fam='1',
            name='test',
            otc='1',
            phone='1234567890',
        )
        self.coords = Coords.objects.create(
            latitude=123,
            longitude=123,
            height=123
        )
        self.level = Level.objects.create(
            winter='1',
            summer='1',
            autumn='1',
            spring='1'
        )
        self.pereval = Pereval.objects.create(
            user=self.user,
            coords=self.coords,
            level=self.level,
        )
        self.images = Images.objects.create(
            data='test',
            title='test',
            pereval=self.pereval
        )
        self.pereval.save()
        url = reverse('pereval-detail', args=[self.pereval.id])
        response1 = self.client.get(url, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['id'], self.pereval.id)
        self.assertEqual(response1.data['coords']['latitude'], self.pereval.coords.latitude)

        data = {
            'coords': {
                'latitude': 1234,
                'longitude': 1234,
                'height': 1234
            }
        }
        response2 = self.client.patch(url, data=data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get(url, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data['coords']['latitude'], self.pereval.coords.latitude)
