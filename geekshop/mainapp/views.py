import json
import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    title = 'главная'

    products = Product.objects.all()[4:7]

    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    content = {
        'title': title,
        'products': products,
        'basket': basket
    }

    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'

    links_menu = ProductCategory.objects.all()

    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category_item,
            'products': products_list,
            'basket': basket
        }

        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[4:10]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'о нас'

    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    locations = []
    with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contacts.json'), encoding='utf-8') as file:
        locations = json.load(file)

    content = {
        'title': title,
        'locations': locations,
        'basket': basket
    }

    return render(request, 'mainapp/contact.html', content)

# Create your views here.
