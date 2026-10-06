from django.http import HttpResponse

def rooms(request):
    return HttpResponse("Список блюд")

def room_detail(request, dish_id):
    return HttpResponse(f"Помещение {dish_id}")