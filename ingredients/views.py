from django.http import HttpResponse

def bookings(request):
    return HttpResponse("Список ингедиентов")

def booking_detail(request, ingredient_id):
    return HttpResponse(f"Бронирование {ingredient_id}")
