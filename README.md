# RE-OWNED — Second-Hand Marketplace

A Django-powered marketplace for buying and selling pre-loved items.

## Features
- 🛍 Browse & search listings with advanced filters
- 📦 Post items for sale with multiple photos
- 🛒 Shopping cart & checkout
- ❤️ Wishlist / save items
- 👤 User profiles & seller pages
- 🔐 Login / Register / Auth
- 📋 Order management
- 🔧 Django Admin panel

## Apps
- `apps/accounts` — Custom user model, profiles, auth
- `apps/listings` — Products, categories, wishlist, filters
- `apps/cart` — Shopping cart with context processor
- `apps/orders` — Checkout and order history

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your SECRET_KEY

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

## Initial Data (via Admin)
1. Go to `/admin/`
2. Add Categories: Clothing, Electronics, Furniture, Sports
3. Set icons: `shirt`, `laptop`, `house`, `trophy`

## Tech Stack
- Django 4.2
- Bootstrap 5.3
- django-filter
- Pillow
- WhiteNoise
