from io import BytesIO
from celery import shared_task 
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from django.utils.translation import gettext_lazy as _


@shared_task 
def payment_completed(order_id):
    """
    funkcja wysyła email o pomyślnym utworzeniu zamówienia
    """
    order = Order.objects.get(id = order_id)
    # utworzenie wiadomości email z rachunkiem
    subject = _('Mój sklep - zamówienie nr {}').format(order.id)
    message = _('W załączniku przesyłamy rachunek dla ostatniego zakupu.\n\nDziękujemy, że zdecydowałeś/aś się na zakupy w naszym sklepie!')
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])
    # wygenerowanie dokumentu PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets = stylesheets)
    # dołączanie pliku w formacie PDF
    email.attach('order_{}'.format(order.id), out.getvalue(), 'application/pdf')
    # wysyłanie wiadomości email
    email.send()