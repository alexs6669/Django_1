import json
import os

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]
    content = {
        'title': title,
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    same_products = Product.objects.all()[:3]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'о нас'
    locations = []
    with open(os.path.join(settings.BASE_DIR, 'contacts.json'), encoding='utf-8') as file:
        locations = json.load(file)
    content = {
        'title': title,
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)


# Create your views here.
