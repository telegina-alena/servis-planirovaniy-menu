from django.http import HttpResponse
from homepage.views import page
from storage import load_ingredients

def ingredients(request):
    ingredients_list = load_ingredients()
    
    items = ""
    for ing in ingredients_list:
        items += f'<li class="list-group-item">[{ing.id}] {ing.name}</li>'
        
    content = f"""
    <h1>Доступные ингредиенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Ингредиенты - Кулинарная книга", content))