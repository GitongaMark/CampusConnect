from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)
   
  def __str__(self):
      return self.name

  class Meta:
    verbose_name_plural = "Categories"

class Product(models.Model):
  seller = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  category = models.ForeignKey(Category, related_name='listings', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.title} by {self.seller.username}'