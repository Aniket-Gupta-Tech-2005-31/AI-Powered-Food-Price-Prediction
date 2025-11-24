from rest_framework.test import APITestCase
from rest_framework import status
from .models import City, Vegetable, PriceEntry
from django.utils import timezone


class CityAPITestCase(APITestCase):
    def setUp(self):
        self.city = City.objects.create(name='Delhi', state='Delhi')

    def test_get_cities(self):
        response = self.client.get('/api/cities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Delhi')


class VegetableAPITestCase(APITestCase):
    def setUp(self):
        self.vegetable = Vegetable.objects.create(name='Tomato', category='tomato')

    def test_get_vegetables(self):
        response = self.client.get('/api/vegetables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Tomato')


class CurrentPricesAPITestCase(APITestCase):
    def setUp(self):
        self.city = City.objects.create(name='Delhi', state='Delhi')
        self.vegetable = Vegetable.objects.create(name='Tomato', category='tomato')
        self.price = PriceEntry.objects.create(
            vegetable=self.vegetable,
            city=self.city,
            price_per_kg=45.50,
            source='government'
        )

    def test_current_prices(self):
        response = self.client.get('/api/current-prices/?city=Delhi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_current_prices_no_city(self):
        response = self.client.get('/api/current-prices/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
