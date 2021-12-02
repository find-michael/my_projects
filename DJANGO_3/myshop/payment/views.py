from django.shortcuts import render, redirect, get_object_or_404
import braintree
from orders.models import Order, OrderItem
from django.conf import settings
from .tasks import payment_completed
from shop.recommender import Recommender
from shop.models import Product


# utworzenie egzemplarza bramki płatności Braintree
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id = order_id)

    if request.method == 'POST':
        # pobranie tokena nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # utworzenie i przesłanie transakcji
        result = gateway.transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # oznaczenie zamówienia jako opłacone
            order.paid = True
            # zapisanie unikatowego identyfikatora transakcji
            order.braintree_id = result.transaction.id
            order.save()
            # uruchamianie asynchronicznego zadania
            payment_completed.delay(order.id)

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # wygenerowanie tokena
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    order_id = request.session.get('order_id')
    r = Recommender()
    order_items_ids = OrderItem.objects.filter(order = order_id)
    items_list = []
    for order_item_id in order_items_ids:
        items_list.append(Product.objects.get(id=order_item_id.product.id))
    r.products_bought(items_list)
    return render(request, 'payment/done.html', {'order_id': order_id})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')