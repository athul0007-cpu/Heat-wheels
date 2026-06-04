from django.urls import path
from .views import CheckoutView, OrderHistoryView, OrderConfirmationView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('history/', OrderHistoryView.as_view(), name='history'),
    path('confirmation/', OrderConfirmationView.as_view(), name='confirmation'),
]
