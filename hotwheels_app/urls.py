from django.urls import path
from .seo import robots_txt, sitemap_xml
from .views import HomeView, AboutView

app_name = 'hotwheels_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
]
