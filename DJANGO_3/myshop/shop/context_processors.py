from .forms import NewslatterForm

def newsletter_form(request):
    return {'newsletter_form': NewslatterForm()}