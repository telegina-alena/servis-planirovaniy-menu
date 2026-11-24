
from django import forms
from django.db import transaction

from .models import Dish, DishIngredient
from ingredients.models import Ingredient
from meals.models import Meal


class DishFilterForm(forms.Form):
    """Форма фильтрации блюд."""

    q = forms.CharField(
        required=False,
        label="Поиск по названию",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите название блюда",
            }
        ),
    )

    meal = forms.ModelChoiceField(
        queryset=Meal.objects.order_by("name"),
        required=False,
        label="Приём пищи",
        empty_label="Все приёмы пищи",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    max_calories = forms.IntegerField(
        required=False,
        min_value=0,
        label="Максимальная калорийность",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
            }
        ),
    )

    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("name", "По названию"),
            ("calories", "По калорийности"),
            ("meal", "По приёму пищи"),
        ],
        initial="name",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )


class DishCreateForm(forms.ModelForm):
    """Форма создания и редактирования блюда."""

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.order_by("name"),
        required=False,
        label="Ингредиенты",
        widget=forms.SelectMultiple(
            attrs={"class": "form-select"}
        ),
    )

    class Meta:
        model = Dish
        fields = [
            "name",
            "calories",
            "meal",
        ]

        labels = {
            "name": "Название блюда",
            "calories": "Калорийность",
            "meal": "Приём пищи",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "calories": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
            "meal": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["ingredients"].initial = (
                self.instance.ingredients.all()
            )

    def save(self, commit=True):
        """Сохранить блюдо и связанные ингредиенты."""

        dish = super().save(commit=False)

        if commit:
            with transaction.atomic():
                dish.save()
                self.save_m2m()

                DishIngredient.objects.filter(
                    dish=dish
                ).delete()

                DishIngredient.objects.bulk_create([
                    DishIngredient(
                        dish=dish,
                        ingredient=ingredient,
                    )
                    for ingredient in self.cleaned_data.get(
                        "ingredients", []
                    )
                ])
        
    def save(self, commit=True):
        """Сохранить блюдо и связанные ингредиенты."""

        dish = super().save(commit=False)

        def save_ingredients():
            DishIngredient.objects.filter(
                dish=dish
            ).delete()

            DishIngredient.objects.bulk_create([
                DishIngredient(
                    dish=dish,
                    ingredient=ingredient,
                )
                for ingredient in self.cleaned_data.get(
                    "ingredients", []
                )
            ])

        
    def save(self, commit=True):
        """Сохранить блюдо и связанные ингредиенты."""

        dish = super().save(commit=False)

        def save_ingredients():
            DishIngredient.objects.filter(
                dish=dish
            ).delete()

            DishIngredient.objects.bulk_create([
                DishIngredient(
                    dish=dish,
                    ingredient=ingredient,
                )
                for ingredient in self.cleaned_data.get(
                    "ingredients", []
                )
            ])

        if commit:
            with transaction.atomic():
                dish.save()
                save_ingredients()
        else:
            def save_m2m():
                save_ingredients()

            self.save_m2m = save_m2m

        return dish