from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



# Create your views here.


def store(request, category_slug=None):
    # categories = None
    # products = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    # try:
    #     single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    # except Exception as e:
    #     raise e
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter((Q(product_name__icontains=keyword)) |
                                                                        Q(product_description__icontains=keyword))
            products_counts = products.count()
        context = {
            'products': products,
            'product_count': products_counts,
        }
    return render(request, 'store/store.html', context)


