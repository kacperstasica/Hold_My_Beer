from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.image.path)
