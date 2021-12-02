from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):

    name = forms.CharField(
        label=_('Imię'), 
        max_length=30, 
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Jan')
                }
            ))

    email = forms.EmailField(
        label=_('Email'), 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'placeholder': _('przykładowy@email.pl')
                }
            ))

    message = forms.CharField(
        label=_('Wiadomość'), 
        max_length=1000, 
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Witam, mam pytanie...')
                }
            ))