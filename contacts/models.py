from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    CATEGORY_CHOICES = [
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    profile_picture = models.ImageField(upload_to='contact_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # important
    
    class Meta:
        unique_together = ['email', 'user']  # Make email unique per user

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

