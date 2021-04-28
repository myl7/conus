from django.contrib import admin

from .models import UstcCasCredential, ContactInfo


@admin.register(UstcCasCredential)
class UstcCasCredentialAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass
