from django.db import models
from django.db.models import CharField, TextField, ImageField, DecimalField, DateField

from accounts.models import Account


class AuctionCategory(models.Model):
    name = CharField(max_length=128)
    description = TextField()
    logo = ImageField(upload_to='images/auction_categories/')

    class Meta:
        verbose_name_plural = "Auction Categories"

    def __str__(self):
        return self.name


class Auction(models.Model):
    owner = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='auctions')
    title = CharField(max_length=128)
    description = TextField()
    photo = ImageField(upload_to='images/auction_items/')
    category = models.ForeignKey(to=AuctionCategory, on_delete=models.CASCADE, related_name='auctions')
    minimal_price = DecimalField(max_digits=8, decimal_places=2)
    buy_now_price = DecimalField(max_digits=8, decimal_places=2)
    # promoted_status =
    # location =
    auction_start = DateField()
    auction_end = DateField()
    visits_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} | {self.category} | Minimal Price: {self.minimal_price} " \
               f"| Minimal Price: {self.buy_now_price}"
