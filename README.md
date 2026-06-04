# HotWheels Ecommerce Django Project

A modern HotWheels-themed ecommerce platform built with reusable Django apps and clean architecture.

## Architecture
- `core`: homepage, brand storytelling, SEO landing pages
- `accounts`: authentication, profile, login/signup flows
- `products`: category, product catalog, reviews, gallery
- `cart`: shopping cart and pricing logic
- `orders`: checkout, billing, shipping, order history
- `promotions`: coupons, landing banners, campaigns
- `dashboard`: admin analytics and content management
- `support`: contact form, support tickets, FAQs

## Features
- Modular Django apps with reusable templates
- Environment-based config using `django-environ`
- Tailwind-inspired UI scaffold via CDN
- Responsive layout for desktop, tablet, and mobile
- SEO-friendly URLs and meta tag structure
- SQLite for development, PostgreSQL-ready for production

## Setup
1. Create a virtual environment
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If you see `ModuleNotFoundError: No module named 'environ'`, make sure the venv is active or run:
   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver
   ```
2. Copy `.env.example` to `.env` and update secrets
3. Migrate database
   ```powershell
   python manage.py migrate
   ```
4. (Optional) Load sample fixture data
   ```powershell
   python manage.py loaddata fixtures/sample_data.json
   ```
5. Create a superuser
   ```powershell
   python manage.py createsuperuser
   ```
6. Run development server
   ```powershell
   python manage.py runserver
   ```

## Deployment
- Use `DJANGO_SETTINGS_MODULE=hotwheels_project.settings.production`
- Configure environment variables in your host provider
- Serve static files with `collectstatic`

## Notes
- `media/` contains user-uploaded files
- `static/` contains shared CSS, JS, and images
- Use the admin dashboard to manage products, orders, and promotions
