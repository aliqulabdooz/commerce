from django.db import models
from django.shortcuts import reverse
from accounts.models import CustomUser
import uuid


class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    STATIC_CHOICES = (
        ('end', 'ending bid'),
        ('start', 'starting bid'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_product')
    product_name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    starting_bid = models.PositiveIntegerField(null=False, blank=False)
    image_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATIC_CHOICES, default='start')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('auctions:product_detail', args=[self.id])


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, models.CASCADE)
    caption = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    product = models.ManyToManyField(Product, related_name='product_comment')

    def __str__(self):
        return f"{self.author} commented to {self.product.values('product_name')[0]['product_name']}"


class WinnerBid(models.Model):
    code = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    author = models.ForeignKey(CustomUser, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class WatchList(models.Model):
    author = models.ForeignKey(CustomUser, models.CASCADE, related_name='user_watchlist')
    product = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True)


