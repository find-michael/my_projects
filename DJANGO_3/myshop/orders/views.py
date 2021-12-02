from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.delivery_cost = cart.delivery_cost
            order.save()
            for item in cart:
                OrderItem.objects.create(order = order, product = item['product'], price = item['price'], quantity = item['quantity'])

            # usunięcie zawartości koszyka na zakupy
            cart.clear()
            # usunięcie kodu rabatowego z sesji
            request.session['coupon_id'] = None
            # uruchomienie asynchronicznego zadania
            order_created.delay(order.id)
            # umieszczenie zamówienia w sesji
            request.session['order_id'] = order.id
            # przekierowanie do płatności
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response