from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Product, ReviewRating
from .forms import ReviewRatingForm
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from orders.models import OrderProduct



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
    form = ReviewRatingForm()
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except ObjectDoesNotExist:
            order_product = None
    else:
        order_product = None
    reviews = ReviewRating.objects.filter(product__id=single_product.id, status=True)
    reviews_count = ReviewRating.objects.filter(product__id=single_product.id, status=True).aggregate(count=Count('id'))
    rating = ReviewRating.objects.filter(product=single_product.id, status=True).aggregate(average=Avg('rating'))
    average_rating = []
    print(f'Count: {reviews_count}')
    print(f'Rating: {rating}')
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'form': form,
        'order_product': order_product,
        'reviews': reviews,
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


@login_required(login_url='accounts:login')
def submit_review(request, product_id):
    if request.method == "POST":
        # product = get_object_or_404(Product, id=product_id)
        try:
            review_rating = ReviewRating.objects.get(user=request.user, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=review_rating)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review submitted successfully')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                form.user_id = request.user.id,
                form.product_id = product_id,
                form.subject = form.cleaned_data['subject'],
                form.rating = form.cleaned_data['rating'],
                form.review = form.cleaned_data['review'],
                form.ip = request.META.get('REMOTE_ADDR'),
                form.save()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)


