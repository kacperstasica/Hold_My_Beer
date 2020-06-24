from PIL import Image
from django.contrib.auth.models import User
from django.db.models import Avg
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
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, choices=RATING_CHOICES)

    def __str__(self):
        return '{} review'.format(self.beer)

    def get_absolute_url(self):
        return reverse('beers:review', kwargs={'pk': self.pk})

    @classmethod
    def count_rating(cls, beer_id):
        return cls.objects.filter(beer_id=beer_id).aggregate(Avg('rating')).get('rating__avg', 0)
