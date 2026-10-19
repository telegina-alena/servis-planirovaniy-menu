from django.http import HttpResponse
from homepage.views import page
from storage import load_dishes, load_ingredients
from models.dishes import find_dish_by_id

def dishes(request):
    # Загружаем список блюд (используя вашу функцию из storage.py)
    dishes_list = load_dishes()
    
    items = ""
    for dish in dishes_list:
        # Формируем ссылку на детальную страницу
        text = f"<strong>{dish.name}</strong> (Калорийность: {dish.calories} ккал, Приём: {dish.meal})"
        items += f'<li class="list-group-item"><a href="/dishes/{dish.id}/">{text}</a></li>'
        
    content = f"""
    <h1>Список блюд</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Блюда - Кулинарная книга", content))

def dish_detail(request, dish_id):
    dishes_list = load_dishes()
    dish = find_dish_by_id(dishes_list, dish_id)
    
    # Обработка случая, если блюдо не найдено (п. 5.4.8)
    if dish is None:
        content = """
        <h1 class="text-danger">Блюдо не найдено</h1>
        <a href="/dishes/" class="btn btn-outline-secondary">← к списку блюд</a>
        """
        return HttpResponse(page("Блюдо не найдено", content), status=404)
    
    # Достаем ингредиенты для проверки (используем вашу функцию)
    ingredients_list = load_ingredients()
    # Используем ваш метод is_available из модели Dish
    # (Предполагается, что ingredient_names возвращает список имен)
    from storage import ingredient_names
    availability_text = dish.is_available(ingredient_names(ingredients_list))
    
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{dish.name}</h5>
            <p class="card-text"><strong>ID:</strong> {dish.id}</p>
            <p class="card-text"><strong>Калорийность:</strong> {dish.calories} ккал</p>
            <p class="card-text"><strong>Приём пищи:</strong> {dish.meal}</p>
            <p class="card-text"><strong>Ингредиенты:</strong> {", ".join(dish.ingredients)}</p>
            <p class="card-text"><strong>Наличие ингредиентов:</strong> {availability_text}</p>
            <a href="/dishes/" class="btn btn-outline-secondary">← к списку блюд</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"{dish.name} - Кулинарная книга", content), status=200)