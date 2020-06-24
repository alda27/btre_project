from django.contrib import admin
from .models import Contact
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'name', 'email')
    list_display_links = ('listing', 'name', 'email')


admin.site.register(Contact, ContactAdmin)