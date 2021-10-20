from django.db import models
from django.db.models import DecimalField, CharField, DateTimeField
from accounts.models import Account
from auctions.models import Auction


class Bid(models.Model):
    item = models.ForeignKey(to=Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='bids')
    amount_to_pay = DecimalField(max_digits=8, decimal_places=2)
    TYPES = (
        ("BID", "Place Bid"),
        ("BYN", "Buy Now")
    )
    bid_type = CharField(
        max_length=3,
        choices=TYPES,
        default="BID"
    )

    def __str__(self):
        return f"{self.bidder} | {self.item} | Minimal Price: {self.amount_to_pay}"


class Purchase(models.Model):
    bid = models.OneToOneField(to=Bid, on_delete=models.CASCADE, related_name='purchase')
    time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid.bidder} | {self.bid.item} | Purchase Price: {self.bid.amount_to_pay}"