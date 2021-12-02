from __future__ import absolute_import, unicode_literals
from celery import shared_task 
from django.core.mail import send_mail
from .models import Order
from myshop.settings import EMAIL_HOST_USER
from django.utils.translation import gettext_lazy as _

@shared_task
def order_created(order_id):
    """
    zadanie wysyłające powiadomienie za pomocą wiadomości e-mail po zakończonym powodzeniem utworzeniu obiektu zamówienia
    """
    order = Order.objects.get(id = order_id)
    subject = _('Zamówienie nr {}').format(order.id)
    message = _('Witaj, {}!\n\nZłożyłeś zamówienie w naszym sklepie.\n\nIdentyfikator twojego zamówienia to {}').format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, EMAIL_HOST_USER, [order.email])
    return mail_sent

