from django.db import models
from users.models import CustomUser

class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=7, decimal_places=2, help_text="Area in square meters")
    images = models.ImageField(upload_to='property_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    def date_posted(self):
        return self.created_at.strftime('%Y-%m-%d')
    def __str__(self):
        return self.title


class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="preference")
    location = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=50, blank=True, null=True, choices=Property.PROPERTY_TYPES)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"