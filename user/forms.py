from django import forms
from django.core.validators import EmailValidator


class ContactInfoUpdateEmailForm(forms.Form):
    email = forms.CharField(max_length=120, validators=[EmailValidator(allowlist=[])])
