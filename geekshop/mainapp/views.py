from django.shortcuts import render


def main(request):
    content = {
        'title': 'главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    content = {
        'title': 'каталог',
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'mainapp/contact.html', content)


# Create your views here.
