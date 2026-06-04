from django.http import HttpResponse
from django.urls import reverse

from products.models import Product


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        f"Sitemap: {request.build_absolute_uri(reverse('hotwheels_app:sitemap'))}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    urls = [
        request.build_absolute_uri(reverse('hotwheels_app:home')),
        request.build_absolute_uri(reverse('hotwheels_app:about')),
        request.build_absolute_uri(reverse('products:list')),
        request.build_absolute_uri(reverse('promotions:list')),
        request.build_absolute_uri(reverse('support:contact')),
    ]
    urls.extend(
        request.build_absolute_uri(reverse('products:detail', kwargs={'slug': product.slug}))
        for product in Product.objects.filter(is_active=True).only('slug')
    )
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    body.extend(f'<url><loc>{url}</loc></url>' for url in urls)
    body.append('</urlset>')
    return HttpResponse('\n'.join(body), content_type='application/xml')
