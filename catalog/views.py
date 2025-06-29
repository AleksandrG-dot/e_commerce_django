from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except:
        return HttpResponse(f"Товар с номером ID {pk} не найден!")
    context = {'product_id': pk, 'product': product}
    return render(request, 'catalog/product_detail.html', context)
