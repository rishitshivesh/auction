from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    product_name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    product_type = models.CharField(max_length=64)
    #category = models.ManyToManyField(Categories,blank=False,related_name="categories")
    # bids = models.IntegerField
    #bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mybids")
    bid_user = models.CharField(max_length=64)
    url = models.CharField(max_length=2000,default="https://icon-library.com/images/products-icon-png/products-icon-png-25.jpg")
    date = models.DateField(auto_now_add="True")
    listed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_name} ({self.date})"
    class Meta:
        verbose_name = 'Auction Listing'

class Categories(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"
    class Meta:
        verbose_name = 'Categorie'
        
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bidder")
    product = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name = "item")
    bid = models.IntegerField()
    class Meta:
        verbose_name = 'Bid'
class Comments(models.Model):
    comment = models.TextField()
    #product_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="product_id")
    product = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name = "comment_item")
    #user = models.ManyToManyField(User,blank=False,related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comment_user")
    date = models.DateTimeField(auto_now_add="True")
    def __str__(self):
        return f"{self.user} : {self.comment}({self.date})"
    class Meta:
        verbose_name = 'Comment'

class Wishlist(models.Model):
    product = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    def __str__(self):
        return f"{self.product} : {self.user}"

