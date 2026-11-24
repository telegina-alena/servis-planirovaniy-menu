
from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):

    def test_homepage(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_dishes_page(self):
        response = self.client.get(reverse("dishes:list"))
        self.assertEqual(response.status_code, 200)

    def test_ingredients_page(self):
        response = self.client.get(reverse("ingredients"))
        self.assertEqual(response.status_code, 200)

    def test_meals_page(self):
        response = self.client.get(reverse("meals"))
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_dish(self):
        response = self.client.get("/dishes/999999/")
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_ingredient(self):
        response = self.client.get("/ingredients/999999/")
        self.assertEqual(response.status_code, 404)
