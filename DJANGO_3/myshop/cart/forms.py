from django import forms
from django.utils.translation import gettext_lazy as _

product_acceptable_cart_add_quantity = 10
product_acceptable_form_quantity_choices = [(i, str(i)) for i in range(1, product_acceptable_cart_add_quantity + 1)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices = product_acceptable_form_quantity_choices, coerce = int, label = _('Ilość'))
    update = forms.BooleanField(required = False, initial = False, widget = forms.HiddenInput)