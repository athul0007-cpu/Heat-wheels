from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from cart.models import Cart
from accounts.utils import is_shop_customer
from promotions.models import Coupon
from .models import Order, OrderItem


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_shop_customer(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('hotwheels_app:home')
        return super().handle_no_permission()


class CheckoutView(CustomerRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get_coupon(self, coupon_code):
        if not coupon_code:
            return None, ''

        now = timezone.now()
        coupon = Coupon.objects.filter(active=True, code__iexact=coupon_code).first()
        if not coupon:
            return None, 'That coupon is not active.'
        if coupon.start_date and coupon.start_date > now:
            return None, 'That coupon is not active yet.'
        if coupon.end_date and coupon.end_date < now:
            return None, 'That coupon has expired.'
        return coupon, ''

    def get_checkout_context(self, request, cart, coupon_code=''):
        coupon_code = coupon_code.strip()
        subtotal = cart.total_price() if cart else Decimal('0.00')
        coupon, coupon_error = self.get_coupon(coupon_code)
        discount_amount = Decimal('0.00')
        if coupon:
            discount_amount = subtotal * Decimal(coupon.discount_percent) / Decimal('100')

        return {
            'cart': cart,
            'coupon_code': coupon_code,
            'coupon': coupon,
            'coupon_error': coupon_error,
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'total_amount': subtotal - discount_amount,
            'shipping_address': request.POST.get('shipping_address', ''),
            'billing_address': request.POST.get('billing_address', ''),
            'payment_method': request.POST.get('payment_method', 'cod'),
        }

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        return render(request, self.template_name, self.get_checkout_context(request, cart))

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return redirect('cart:detail')

        shipping_address = request.POST.get('shipping_address', '').strip()
        billing_address = request.POST.get('billing_address', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        if request.POST.get('action') == 'apply_coupon':
            context = self.get_checkout_context(request, cart, coupon_code)
            if context['coupon']:
                messages.success(request, f'{context["coupon"].code} applied successfully.')
            elif coupon_code:
                messages.error(request, context['coupon_error'])
            else:
                messages.error(request, 'Enter a coupon code to apply.')
            return render(request, self.template_name, context)

        if not shipping_address or not billing_address:
            messages.error(request, 'Please enter both shipping and billing addresses.')
            return render(request, self.template_name, self.get_checkout_context(request, cart, coupon_code))

        with transaction.atomic():
            items = list(cart.items.select_related('product').select_for_update())
            for item in items:
                if item.quantity > item.product.stock:
                    messages.error(request, f'Only {item.product.stock} left for {item.product.title}.')
                    return redirect('cart:detail')

            subtotal = sum(item.total_price() for item in items)
            discount_amount = Decimal('0.00')
            coupon, coupon_error = self.get_coupon(coupon_code)
            if coupon_error:
                messages.error(request, coupon_error)
                return render(request, self.template_name, self.get_checkout_context(request, cart, coupon_code))
            if coupon:
                discount_amount = subtotal * Decimal(coupon.discount_percent) / Decimal('100')

            order = Order.objects.create(
                user=request.user,
                total_amount=subtotal - discount_amount,
                shipping_address=shipping_address,
                billing_address=billing_address,
                payment_method=payment_method,
                payment_status='pending' if payment_method == 'cod' else 'paid',
                coupon_code=coupon.code if coupon else '',
                discount_amount=discount_amount,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                )
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])
            cart.items.all().delete()
            request.session['latest_order_id'] = order.id
        return redirect('orders:confirmation')


class OrderHistoryView(CustomerRequiredMixin, TemplateView):
    template_name = 'orders/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-placed_at')
        return context


class OrderConfirmationView(CustomerRequiredMixin, TemplateView):
    template_name = 'orders/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('latest_order_id')
        context['order'] = Order.objects.filter(id=order_id, user=self.request.user).first()
        return context
