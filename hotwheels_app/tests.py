from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product
from support.models import SupportMessage


class SmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Street Racers',
            slug='street-racers',
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Neon Drift Runner',
            slug='neon-drift-runner',
            summary='A fast collector model.',
            description='Built for smoke-test checkout flows.',
            price=Decimal('24.99'),
            stock=3,
            is_active=True,
        )
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='test-password-123',
        )

    def test_public_pages_render(self):
        route_names = [
            'hotwheels_app:home',
            'hotwheels_app:about',
            'products:list',
            'promotions:list',
            'support:contact',
            'accounts:login',
            'accounts:register',
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_customer_pages_redirect_anonymous_users_to_login(self):
        route_names = [
            'accounts:profile',
            'accounts:profile_edit',
            'orders:checkout',
            'orders:history',
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                path = reverse(route_name)
                response = self.client.get(path)
                self.assertRedirects(
                    response,
                    f'{reverse("accounts:login")}?next={path}',
                    fetch_redirect_response=False,
                )

    def test_guest_can_add_product_to_cart(self):
        response = self.client.post(reverse('cart:add', args=[self.product.id]))

        self.assertRedirects(response, reverse('cart:detail'))
        response = self.client.get(reverse('cart:detail'))
        self.assertContains(response, self.product.title)
        self.assertContains(response, 'Qty')

    def test_support_contact_post_creates_message(self):
        response = self.client.post(
            reverse('support:contact'),
            {
                'subject': 'Where is my order?',
                'message': 'Please send an update.',
                'email': 'buyer@example.com',
            },
        )

        self.assertRedirects(response, reverse('support:contact'))
        message = SupportMessage.objects.get()
        self.assertEqual(message.subject, 'Where is my order?')
        self.assertEqual(message.email, 'buyer@example.com')
