from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForProductForm(forms.Form):
    search_input = forms.CharField(
        label='',
        max_length='30',
        widget=forms.TextInput(attrs={'placeholder': _('Wpisz tutaj')})
    )


class NewslatterForm(forms.Form):
    email_input = forms.EmailField(
        label=_('Zapisz się do newslettera!'),
        max_length='50',
        widget=forms.TextInput(attrs={'placeholder': _('Wpisz tutaj swój email')})
    )