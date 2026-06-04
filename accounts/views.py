from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView

from cart.views import merge_guest_cart_to_user
from .forms import CustomSignupForm, LoginForm, ProfileForm
from .models import UserProfile
from .utils import is_shop_customer
from products.models import Product


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('accounts:login')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_shop_customer(self.request.user):
            merge_guest_cart_to_user(self.request, self.request.user)
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('hotwheels_app:home')


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_shop_customer(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('hotwheels_app:home')
        return super().handle_no_permission()


class ProfileView(CustomerRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        orders = self.request.user.orders.prefetch_related('items__product').order_by('-placed_at')
        context['profile'] = profile
        context['recent_orders'] = orders[:4]
        context['order_count'] = orders.count()
        context['wishlist'] = profile.wishlist.filter(is_active=True).prefetch_related('images')[:6]
        context['wishlist_count'] = profile.wishlist.count()
        return context


class UpdateProfileView(CustomerRequiredMixin, View):
    template_name = 'accounts/profile_update.html'

    def get(self, request):
        form = ProfileForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    if not is_shop_customer(request.user):
        return redirect('hotwheels_app:home')

    product = get_object_or_404(Product, id=product_id, is_active=True)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.wishlist.filter(id=product.id).exists():
        profile.wishlist.remove(product)
        messages.success(request, f'{product.title} removed from your wishlist.')
    else:
        profile.wishlist.add(product)
        messages.success(request, f'{product.title} added to your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'accounts:profile'))
