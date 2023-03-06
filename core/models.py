from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=2000)
    img=models.CharField(max_length=2000)
    price=models.FloatField()
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Ordereditem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id=models.CharField(max_length=2000)
    item_name=models.CharField(max_length=2000,default='')
    item_img=models.CharField(max_length=2000,default='')
    item_price=models.FloatField(default=0.0)
    item_category=models.CharField(max_length=100,default='')
    quantity=models.IntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

    @property
    def get_total(self):
        return self.item_price*self.quantity

class Likeditem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id=models.CharField(max_length=2000)
    item_name=models.CharField(max_length=2000,default='')
    item_img=models.CharField(max_length=2000,default='')
    item_price=models.FloatField(default=0.0)
    item_category=models.CharField(max_length=100,default='')
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username