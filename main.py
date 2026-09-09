from datetime import date

dish = "Курица с рисом"
ingredients = ['рис', 'курица', 'приправы', 'соль', 'масло', 'овощи']
day_of_week = '2026-09-09'
meal = 'обед'


def check_dish_availability(dish, ingredients): #проверка на наличие всех ингридиентов
    available_ingredients = ['рис', 'курица', 'приправы', 'соль', 'масло', 'овощи']
    missing = []
    for ing in ingredients:
        if ing not in available_ingredients:
            missing.append(ing)
    
    if missing:
        return f"Не хватает ингредиентов: {', '.join(missing)}"
    else:
        return f"Все ингредиенты есть! Можно готовить {dish}"



