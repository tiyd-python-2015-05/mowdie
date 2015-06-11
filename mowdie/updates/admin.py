from django.contrib import admin
from .models import Update, Favorite

class UpdateAdmin(admin.ModelAdmin):
    list_display = ['text', 'user']

# Register your models here.
admin.site.register(Update, UpdateAdmin)
admin.site.register(Favorite)

