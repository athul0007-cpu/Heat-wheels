from django.views.generic import TemplateView

from products.models import Product
from .models import Coupon, Promotion


class PromotionListView(TemplateView):
    template_name = 'promotions/promotions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promotions'] = Promotion.objects.filter(is_live=True).order_by('-launch_date')
        context['coupons'] = Coupon.objects.filter(active=True).order_by('code')
        context['featured_products'] = Product.objects.filter(is_active=True, featured=True).order_by('-created_at')[:6]
        return context
