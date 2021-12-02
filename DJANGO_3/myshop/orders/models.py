from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_('Imię'), max_length=50)
    last_name = models.CharField(_('Nazwisko'), max_length=50)
    email = models.EmailField(_('E-mail'),)
    address = models.CharField(_('Adres'), max_length=250)
    postal_code = models.CharField(_('Kod_pocztowy'), max_length=20)
    city = models.CharField(_('Miejscowość'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return round(total_cost - (total_cost * (self.discount / Decimal(100))) + self.delivery_cost, 2)

    def get_discounted_value(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return round(total_cost * (self.discount / Decimal(100)), 2)

    braintree_id = models.CharField(max_length=150, blank=True)

    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
