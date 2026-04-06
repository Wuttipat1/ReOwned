from django.db import models
from django.conf import settings
from apps.listings.models import Listing


class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_seller')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['listing', 'buyer']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.buyer.username} → {self.seller.username} ({self.listing.title})"

    @property
    def last_message(self):
        return self.messages.last()

    @property
    def unread_count_for(self):
        return self.messages.filter(is_read=False)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.body[:40]}"
