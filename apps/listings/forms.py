from django import forms
from .models import Listing, ListingImage


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'condition', 'category', 'brand', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']


ListingImageFormSet = forms.inlineformset_factory(
    Listing, ListingImage,
    form=ListingImageForm,
    extra=4,
    max_num=8,
    can_delete=True
)
