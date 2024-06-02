from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from store.models import Product,Variation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .forms import BillingForm




# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    current_user = request.user
    # If user is authenticated
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)  # Get the product
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variations = Variation.objects.get(product=product, variation_category__iexact=key,
                                                       variation_value__iexact=value)
                    product_variation.append(variations)
                except ObjectDoesNotExist:
                    pass
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variation_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # Increase cart quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect("carts:cart")
    # If the user is not authenticated
    else:
        product = get_object_or_404(Product, id=product_id)  # Get the product
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variations = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variations)
                except ObjectDoesNotExist:
                    pass
        cart_obj, created = Cart.objects.get_or_create(cart_id=_cart_id(request)) # get or create the cart using the cart ID present in the session
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart_obj).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart_obj)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variation_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # Increase cart quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart_obj)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart_obj
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect("carts:cart")


def remove_cart(request, product_id, cart_item_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except ObjectDoesNotExist:
            pass
        return redirect("carts:cart")
    else:
        cart_ = Cart.objects.get(cart_id=_cart_id(request))
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart_, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except ObjectDoesNotExist:
            pass
        return redirect("carts:cart")


def remove_cart_item(request, product_id, cart_item_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if current_user.is_authenticated:
        cart_items = CartItem.objects.get(user=current_user, product=product, id=cart_item_id)
        cart_items.delete()
        return redirect("carts:cart")
    else:
        cart_ = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.get(cart=cart_, product=product, id=cart_item_id)
        cart_items.delete()
        return redirect("carts:cart")


def cart(request, total=0, quantity=0, cart_items=0):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_ = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='accounts:login')
def checkout(request, total=0, quantity=0, cart_items=0):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_ = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    form = BillingForm()
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'form': form
    }
    return render(request, 'store/checkout.html', context)
