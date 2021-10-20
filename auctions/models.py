from django.db import models
from django.db.models import CharField, TextField, ImageField, DecimalField, DateTimeField
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
    auction_start = DateTimeField()
    auction_end = DateTimeField()
    visits_number = models.IntegerField(default=0)
    TYPES = (
        ("STA", "Auction Started"),
        ("EXP", "Auction Expired"),
        ("PUR", "Item Purchased")
    )
    auction_status = CharField(
        max_length=3,
        choices=TYPES,
        default="STA"
    )

    def __str__(self):
        return f"{self.title} | {self.category} | Minimal Price: {self.minimal_price} " \
               f"| Buy Now Price: {self.buy_now_price}"
