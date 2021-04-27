from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from social_core.utils import user_is_active

from mainapp.models import Product
from basketapp.models import Basket


@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
    content = {
        'title': 'корзина',
        'basket_items': basket_items
    }

    return render(request, 'basketapp/basket.html', content)


# class BasketCreateView(UpdateView):
#     model = Basket
#
#     def get_object(self, **kwargs):
#         basket_item = Basket.objects.filter(user=self.request.user, product__pk=self.kwargs['pk']).first()
#         if not basket_item:
#             basket_item = Basket.objects.create(user=self.request.user, product__pk=self.kwargs['pk'])
#         basket_item.quantity += 1
#         basket_item.save()
#         return basket_item
#
#     def form_valid(self, form):
#         return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
#
#     @method_decorator(user_is_active(lambda u: u.is_active))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    old_basket_item = Basket.objects.filter(product=product, user=request.user).first()

    if old_basket_item:
        # old_basket_item[0].quantity += 1
        old_basket_item[0].quantity = F('quantity') + 1
        old_basket_item[0].save()

        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'query basket_add: {update_queries}')
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

        content = {
            'basket_items': basket_items
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
