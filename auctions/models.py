from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    image = models.CharField(max_length=120)
    first_bid =models.IntegerField(default=0)


class Bid(models.Model):
    listing_id=models.ForeignKey(Listing,on_delete=CASCADE,related_name="all_bids")
    current_bid = models.IntegerField()
    def __str__(self):
        return f" {self.listing_id} {self.current_bid} "