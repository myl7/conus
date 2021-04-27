from django.contrib import admin

from .models import UstcCasCredential


@admin.register(UstcCasCredential)
class UstcCasCredentialAdmin(admin.ModelAdmin):
    pass
