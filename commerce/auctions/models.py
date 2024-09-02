from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, default = 'Other')
    def __str__(self):
        return self.name
    


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    url = models.CharField(max_length=64, null=True, blank=True) 
    status = models.BooleanField(null=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.title
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.listing.title}" 


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.listing.title} ({self.amount})" 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments') 
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True) 
    content = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.user.username} - {self.listing.title} ({self.content})" 
