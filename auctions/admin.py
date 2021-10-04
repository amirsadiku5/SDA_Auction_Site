from django.contrib import admin
from .models import AuctionCategory, Auction

admin.site.register(AuctionCategory)
admin.site.register(Auction)
