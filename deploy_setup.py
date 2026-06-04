import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotwheels_project.settings.production')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    # Read credentials from environment variables, fallback to defaults
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword123')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully!")
    else:
        print(f"Superuser '{username}' already exists. Updating password.")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Superuser password updated successfully!")

if __name__ == '__main__':
    create_superuser()
