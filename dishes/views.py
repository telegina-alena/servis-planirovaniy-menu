from django.http import HttpResponse

def dishes(request):
    return HttpResponse("Список блюд")

def dish_detail(request, dish_id):
    return HttpResponse(f"Блюдо {dish_id}")