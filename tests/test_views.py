
from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):

    def test_homepage(self):
        response = self.client.get(
            reverse("homepage:index")
        )
        self.assertEqual(response.status_code, 200)

    def test_dishes_page(self):
        response = self.client.get(
            reverse("dishes:list")
        )
        self.assertEqual(response.status_code, 200)

    def test_ingredients_page(self):
        response = self.client.get(
            reverse("ingredients:ingredients")
        )
        self.assertEqual(response.status_code, 200)

    def test_meals_page(self):
        response = self.client.get(
            reverse("meals:meals")
        )
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_dish(self):
        response = self.client.get(
            reverse("dishes:detail", args=[999999])
        )
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_ingredient(self):
        response = self.client.get(
            reverse("ingredients:ingredient_detail", args=[999999])
        )
        self.assertEqual(response.status_code, 404)