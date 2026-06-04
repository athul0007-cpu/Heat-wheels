from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

FIELD_CLASSES = 'w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 focus:ring-2 focus:ring-orange-500'


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': FIELD_CLASSES}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': FIELD_CLASSES}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASSES}))


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': FIELD_CLASSES}))
    phone = forms.CharField(max_length=24, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    city = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    pincode = forms.CharField(max_length=12, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASSES}))
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={**{'rows': 3}, **{'class': FIELD_CLASSES}}),
    )
    favorite_collection = forms.CharField(
        label='Favorite collection',
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={'class': FIELD_CLASSES}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        if user and not args and 'initial' not in kwargs:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            kwargs['initial'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone,
                'city': profile.city,
                'pincode': profile.pincode,
                'address': profile.address,
                'favorite_collection': profile.favorite_collection,
            }
        super().__init__(*args, **kwargs)

    def save(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.save(update_fields=['first_name', 'last_name', 'email'])

        profile.phone = self.cleaned_data['phone']
        profile.city = self.cleaned_data['city']
        profile.pincode = self.cleaned_data['pincode']
        profile.address = self.cleaned_data['address']
        profile.favorite_collection = self.cleaned_data['favorite_collection']
        profile.save(update_fields=['phone', 'city', 'pincode', 'address', 'favorite_collection'])
        return self.user
