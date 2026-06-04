from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from products.models import Product
from accounts.utils import is_shop_customer
from .models import Cart, CartItem


def get_or_create_cart(request):
    if is_shop_customer(request.user):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
        if cart:
            return cart

    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return cart


def merge_guest_cart_to_user(request, user):
    cart_id = request.session.pop('cart_id', None)
    if not cart_id:
        return

    guest_cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
    if not guest_cart:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)
    for guest_item in guest_cart.items.select_related('product'):
        item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=guest_item.product,
            defaults={'quantity': guest_item.quantity},
        )
        if not created:
            item.quantity = min(item.quantity + guest_item.quantity, guest_item.product.stock)
            item.save()
    guest_cart.delete()


class CartView(View):
    template_name = 'cart/cart_detail.html'

    def get(self, request):
        cart = get_or_create_cart(request)
        return render(request, self.template_name, {
            'cart': cart,
            'cart_items': cart.items.all(),
            'total': cart.total_price(),
        })


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if product.stock < 1:
            messages.error(request, 'This product is currently out of stock.')
            return redirect('products:detail', slug=product.slug)

        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if item.quantity >= product.stock:
                messages.info(request, 'You already have the available stock in your cart.')
                return redirect('cart:detail')
            item.quantity += 1
            item.save()
        return redirect('cart:detail')


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect('cart:detail')


class UpdateCartView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        item.quantity = min(max(1, quantity), item.product.stock)
        item.save()
        return redirect('cart:detail')
