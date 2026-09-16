from datetime import date

dish = "Курица с рисом"
ingredients = ['рис', 'курица', 'приправы']
all_ingredients = ['рис', 'курица', 'соль', 'масло', 'овощи']
day_of_week = '2026-09-09'
meal = 'обед'
dish_calories = 200 


def check_dish_availability(dish, ingredients, all_ingredients): #проверка на наличие всех ингридиентов
    missing = []
    for ing in ingredients:
        if ing not in all_ingredients:
            missing.append(ing)
    
    if missing:
        return f"Не хватает ингредиентов: {', '.join(missing)}"
    else:
        return f"Все ингредиенты есть! Можно готовить {dish}"

def get_calories_per_portion(dish, dish_calories, portions=1): #рассчет каллориев на одну порцию
    if portions > 0:
        per_portion = dish_calories // portions
    else: 
        return 0
    
    if per_portion <= 200:
        return f"{dish} - {per_portion} ккал - легкое блюдо"
    elif per_portion <= 400:
        return f"{dish} - {per_portion} ккал - средняя калорийность"
    else:
        return f"{dish} - {per_portion} ккал - калорийное блюдо"

def get_serving_suggestion(meal): #сервировка блюда
    suggestions = {
        'завтрак': 'Подавать на маленькой тарелке',
        'обед': 'Подавать на большой тарелке с гарниром',
        'ужин': 'Подавать на средней тарелке'
    }
    return suggestions.get(meal.lower(), '🍽️ Подавать на тарелке')

print(check_dish_availability(dish, ingredients, all_ingredients))
print(get_calories_per_portion(dish, dish_calories))
print(get_serving_suggestion(meal))