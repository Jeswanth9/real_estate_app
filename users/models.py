from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='Phone Number')
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username