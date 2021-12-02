from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from myshop.settings import EMAIL_HOST_USER


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name'].capitalize()

            body = {
			'name': name, 
			'email': cd['email'], 
			'message': cd['message'], 
			}

            message = "\n\n".join('{} : {}'.format(key, value) for key, value in body.items())

            send_mail(
                f'{name} wysłał wiadomość email', message, EMAIL_HOST_USER, [EMAIL_HOST_USER]
            )
            form = ContactForm()
            return render(request, 'contact/contact.html', {'form': form, 'success': True})
    else: 
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})