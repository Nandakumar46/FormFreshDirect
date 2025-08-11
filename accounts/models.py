# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('FARMER', 'Farmer'),
        ('CLIENT', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# Use a signal to create a Profile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Default to Client if not specified during signup
        Profile.objects.create(user=instance, user_type='CLIENT')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()