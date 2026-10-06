from django.http import HttpResponse


def index(request):
 return HttpResponse("Менюшка - сервис планирования меню")
