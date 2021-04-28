from django import forms
from django.contrib.auth.models import User

from .models import Notice


class NoticeCreateForm(forms.ModelForm):
    to_users = forms.ModelMultipleChoiceField(User.objects.filter(is_staff=False))
    title = forms.CharField(max_length=60, required=False)
    body = forms.CharField(max_length=510)

    class Meta:
        model = Notice
        exclude = ['from_user']
