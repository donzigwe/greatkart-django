from django.db import models
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to="photos/product")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_details', args=[self.category.slug, self.slug])
