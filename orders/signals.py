from django.shortcuts import get_object_or_404
from .models import Order, Payment, OrderProduct
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver

from carts.models import CartItem


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        order = get_object_or_404(Order, order_number=ipn.invoice)
        payment = Payment.objects.create(
            user=order.user,
            payment_id=ipn.invoice,
            payment_method='paypal',
            amount_paid=ipn.mc_gross,
            status=ipn.payment_status)
        payment.save()

        if order.grand_total == ipn.mc_gross:
            # mark the order as paid
            order_payment = get_object_or_404(Payment, payment_id=ipn.invoice)
            order.is_ordered = True
            order.payment = order_payment
            order.save()
            cart_items = CartItem.objects.filter(user=order.user)

            for item in cart_items:
                ordered_products = OrderProduct.objects.create(
                    order=order,
                    payment=order_payment,
                    user=item.user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    is_ordered=True
                )
                ordered_products.save()