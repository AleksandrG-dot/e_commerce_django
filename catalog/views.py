from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse(f"Товар с номером ID {product_id} не найден!")
    context = {'product_id': product_id,'product': product}
    return render(request, 'catalog/product_detail.html', context)
