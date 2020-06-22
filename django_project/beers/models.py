from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Beer(models.Model):
    product_name = models.CharField(max_length=140)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    alcohol = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(default='default_beer.jpg', upload_to='beer_labels')

    class Meta:
        verbose_name = 'beer'
        verbose_name_plural = 'beers'

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Review(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    def __str__(self):
        return '{} review'.format(self.beer)

    def get_absolute_url(self):
        return reverse('beers:review', kwargs={'pk': self.pk})
