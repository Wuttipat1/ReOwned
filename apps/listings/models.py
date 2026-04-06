from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('listings_by_category', kwargs={'slug': self.slug})


class Listing(models.Model):
    CONDITION_CHOICES = [
        ('like_new', 'Like New'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('poor', 'Poor'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    brand = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})

    @property
    def main_image(self):
        img = self.images.first()
        return img.image if img else None

    @property
    def condition_display(self):
        return dict(self.CONDITION_CHOICES).get(self.condition, self.condition)


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.listing.title}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']

    def __str__(self):
        return f"{self.user.username} -> {self.listing.title}"
