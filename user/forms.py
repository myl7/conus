from django import forms

from .models import ContactInfo


class ContactInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        exclude = []
