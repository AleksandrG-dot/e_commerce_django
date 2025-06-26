from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(requests):
    if requests.method == 'POST':
        name = requests.POST.get('name')
        phone = requests.POST.get('phone')
        message = requests.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(requests, 'catalog/contacts.html')
