from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from django.contrib.auth.models import User
from orders.models import Order
from products.models import Product
from promotions.models import Promotion
from support.models import SupportMessage


@staff_member_required
def dashboard_home(request):
    context = {
        'product_count': Product.objects.count(),
        'order_count': Order.objects.count(),
        'user_count': User.objects.count(),
        'promotion_count': Promotion.objects.count(),
        'open_support_count': SupportMessage.objects.filter(resolved=False).count(),
        'recent_orders': Order.objects.select_related('user').order_by('-placed_at')[:5],
    }
    return render(request, 'dashboard/dashboard_home.html', context)
