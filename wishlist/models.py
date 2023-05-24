from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
# wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.product) 