from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('payments', views.payments, name='payments'),
    path('payment_successful/<order_number>', views.payment_successful, name='payment_successful'),
    path('payment_failed/<order_number>', views.payment_failed, name='payment_failed'),


]