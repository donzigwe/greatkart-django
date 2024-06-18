from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Order, Payment, OrderProduct
from .forms import OrderForm
# Paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from carts.models import CartItem
from GreatKart.functions import order_id

from store.models import Product


def payments(request):
    return render(request, 'orders/payments.html')


# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store:store')
    # tax = 0
    # grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = total * 0.02
    grand_total = tax + total
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.total = total
            data.tax = tax
            data.grand_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            order_number = order_id()
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            host = request.get_host()
            print(order.order_number)
            paypal_checkout = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': order.grand_total,
                'item_name': f'{order.first_name} {order.last_name}',
                'invoice': order.order_number,
                "notify_url": f"http://{host}{reverse('paypal-ipn')}",
                "return": f"http://{host}{reverse('orders:payment_successful', kwargs={'order_number': order.order_number})}",
                "cancel_return": f"http://{host}{reverse('orders:payment_failed', kwargs={'order_number': order.order_number})}",

            }
            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'paypal': paypal_payment,
            }
            return render(request, 'orders/payments.html', context)
        else:
            print(form.errors)


@csrf_exempt
def payment_successful(request, order_number):
    order = Order.objects.get(order_number=order_number)

    payment = Payment.objects.create(
        user=order.user,
        payment_id=order_number,
        payment_method='paypal',
        amount_paid=order.grand_total,
        status='Completed')
    payment.save()
    order_payment = get_object_or_404(Payment, payment_id=order_number)
    order.is_ordered = True
    order.payment = order_payment
    order.save()
    # Temporary code!
    # Create OrderProduct
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        #     order_product = OrderProduct()
        #     order_product.order_id = order.id
        #     order_product.payment = order_payment
        #     order_product.user_id = request.user.id
        #     order_product.quantity = item.quantity
        #     order_product.product_price = item.price
        #     order_product.is_ordered = True
        #     order_product.save()

        ordered_products = OrderProduct.objects.create(
            order=order,
            payment=order_payment,
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            is_ordered=True
        )
        ordered_products.save()
        # Update Variations
        cart_item = CartItem.objects.get(id=item.id)
        item_variations = cart_item.variations.all()
        ordered_products = OrderProduct.objects.get(id=ordered_products.id)
        ordered_products.variation.set(item_variations)
        ordered_products.save()
        # Reduce the quantity of carts
        product = Product.objects.get(id=cart_item.product.id)
        product.stock = product.stock-cart_item.quantity
        product.save()
    # Delete Carts
    cart_items.delete()
    # Send order received email to customers
    mail_subject = "GreatKart: Order Received Email"
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = order.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    ordered_items = OrderProduct.objects.filter(order__id=order.id)
    print(ordered_items)
    context = {'order': order, 'items': ordered_items}
    return render(request, 'orders/payment_successful.html', context)


@csrf_exempt
def payment_failed(request, order_number):
    order = Order.objects.get(order_number=order_number)
    payment = Payment.objects.create(
        user=order.user,
        payment_id=order_number,
        payment_method='paypal',
        amount_paid=order.grand_total,
        status='failed')
    payment.save()
    return render(request, 'orders/payment_failed.html', context={'order': order})
