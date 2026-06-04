from django.views.generic import TemplateView

from products.models import Category, Product
from promotions.models import Promotion


class HomeView(TemplateView):
    template_name = 'hotwheels_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_active=True, featured=True).order_by('-created_at')[:3]
        context['new_arrivals'] = Product.objects.filter(is_active=True).order_by('-created_at')[:3]
        context['categories'] = Category.objects.all()[:6]
        context['promotions'] = Promotion.objects.filter(is_live=True).order_by('-launch_date')[:3]
        return context


class AboutView(TemplateView):
    template_name = 'hotwheels_app/about.html'
