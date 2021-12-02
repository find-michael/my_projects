from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon
from .forms import product_acceptable_cart_add_quantity


class Cart(object):

    def __init__(self, request):
        """
        inicjacja koszyka na zakupy
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # zapis pustego koszyka na zakupy w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # zapisanie wykorzystywanego kuponu
        self.coupon_id = self.session.get('coupon_id')
        self.delivery_cost = Decimal(9.99)

    def __iter__(self):
        """
        iteracja przez elementy koszyka na zakupy i pobranie produktów z bazy danych
        """
        product_ids = self.cart.keys()
        # pobranie obiektów produktów i dodanie ich do koszyka na zakupy
        products = Product.objects.filter(id__in = product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        obliczanie wszystkich elementów w koszyku na zakupy
        """
        return sum(item['quantity'] for item in self.cart.values())

    def uniquelen(self):
        """
        obliczanie unikalnych elementów w koszyku na zakupy
        """
        return len(self.cart)

    def add(self, product, quantity = 1, update_quantity = False):
        """
        dodanie produktu do koszyka lub zmiana jego ilości
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            if self.cart[product_id] and self.cart[product_id]['quantity'] + quantity > product_acceptable_cart_add_quantity:
                self.cart[product_id]['quantity'] = product_acceptable_cart_add_quantity
            else:
                self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        """
        usunięcie produktu z koszyka na zakupy
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # usunięcie koszyka na zakupy z sesji
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        # oznaczenie sesji jako zmodyfikowanej, aby upewnić się o jej zapisaniu
        self.session.modified = True 

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id = self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            print((self.coupon.discount / Decimal('100')) * self.get_total_price())
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return round(self.get_total_price() - self.get_discount() + self.delivery_cost, 2)

    
