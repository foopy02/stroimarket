from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Cart(models.Model):
    username = models.CharField(max_length=100)
    product_id = models.IntegerField()
    price = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.username 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    stars = models.IntegerField()
    comment = models.TextField()
    product_id = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

