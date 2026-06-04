from django.db.models import Q
from django.views.generic import DetailView, ListView

from accounts.models import UserProfile
from accounts.utils import is_shop_customer
from .models import Category, Product


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    model = Product
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        queryset = Product.objects.filter(is_active=True)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(summary__icontains=query) | Q(description__icontains=query)
            )
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset.order_by('-featured', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        if is_shop_customer(self.request.user):
            profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
            context['wishlist_ids'] = set(profile.wishlist.values_list('id', flat=True))
        else:
            context['wishlist_ids'] = set()
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_wishlist'] = False
        if is_shop_customer(self.request.user):
            profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
            context['in_wishlist'] = profile.wishlist.filter(id=self.object.id).exists()
        return context
