# In properties/admin.py
from django.contrib import admin
from .models import Property,UserPreference

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'area', 'date_posted')

admin.site.register(Property, PropertyAdmin)
admin.site.register(UserPreference)