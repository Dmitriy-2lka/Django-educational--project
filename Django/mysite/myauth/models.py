from django.db import models
from django.contrib.auth.models import User

def profile_avatar_directory_path(instance: 'Profile', filename: str) -> str:
    return f'profile/profile_{instance.user.pk}/avatar/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio =models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)