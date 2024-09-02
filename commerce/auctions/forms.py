from django.forms import ModelForm
from django import forms
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "category", "url"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"




""" # Creating a form to add an listing.
>>> form = ListingForm()

# Creating a form to change an existing listing.
>>> listing = listing.objects.get(pk=1)
>>> form = ListingForm(instance=listing) """
