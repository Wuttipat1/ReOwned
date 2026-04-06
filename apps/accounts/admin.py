from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rating', 'total_sales', 'is_active']
    list_filter = ['is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('avatar', 'bio', 'phone', 'location', 'rating', 'total_sales')}),
    )
