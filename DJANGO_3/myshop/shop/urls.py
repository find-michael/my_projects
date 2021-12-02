from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(_('cookies/'), views.cookies, name='cookies'),
    path(_('terms/'), views.terms_of_use, name='terms_of_use'),
    path(_('delivery/'), views.delivery, name='delivery'),
    path(_('payment-methods/'), views.payment_methods, name='payment_methods'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]