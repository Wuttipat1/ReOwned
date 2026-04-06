from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, Message
from apps.listings.models import Listing


@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).select_related('listing', 'buyer', 'seller')
    return render(request, 'inbox/inbox.html', {'conversations': conversations})


@login_required
def conversation_view(request, pk):
    conversation = get_object_or_404(
        Conversation, pk=pk
    )
    # Only buyer or seller can view
    if request.user not in [conversation.buyer, conversation.seller]:
        return redirect('inbox')

    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=body,
            )
            conversation.save()  # update updated_at
        return redirect('conversation', pk=pk)

    return render(request, 'inbox/conversation.html', {'conversation': conversation})


@login_required
def start_conversation_view(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, is_active=True)

    # ห้ามคุยกับตัวเอง
    if request.user == listing.seller:
        messages.warning(request, "ไม่สามารถส่งข้อความหาตัวเองได้ครับ")
        return redirect(listing.get_absolute_url())

    # หา conversation ที่มีอยู่แล้ว หรือสร้างใหม่
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        defaults={'seller': listing.seller}
    )

    if created and request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=body,
            )

    return redirect('conversation', pk=conversation.pk)
