from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Newsletter
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import SearchForProductForm, NewslatterForm

def product_list(request, category_slug=None):
    category = None
    search_input = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    search_product_form = SearchForProductForm()
    newsletter_form = NewslatterForm()
    cart_product_form = CartAddProductForm()
    
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        products = products.filter(category=category)

    if request.method == 'GET':
        form = SearchForProductForm(request.GET)
        if form.is_valid():
            search_input = request.GET.get('search_input')
            products = products.filter(translations__name__icontains = search_input).distinct()

    if request.method == 'POST':
        newsletter_form = NewslatterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email_input']
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email = email)
            newsletter_form = NewslatterForm()


    return render(request, 'shop/product/list.html', {
        'category': category, 
        'categories': categories, 
        'products': products, 
        'search_product_form': search_product_form, 
        'search_input': search_input,
        'newsletter_form': newsletter_form,
        'cart_product_form': cart_product_form
        })

def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id, translations__language_code=language, translations__slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'recommended_products': recommended_products})

def cookies(request):
    return render(request, 'shop/cookies.html')

def terms_of_use(request):
    return render(request, 'shop/terms.html')

def delivery(request):
    return render(request, 'shop/delivery.html')

def payment_methods(request):
    return render(request, 'shop/payment_methods.html')
