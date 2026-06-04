from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView, UpdateProfileView, toggle_wishlist

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', UpdateProfileView.as_view(), name='profile_edit'),
    path('wishlist/<int:product_id>/toggle/', toggle_wishlist, name='wishlist_toggle'),
]
