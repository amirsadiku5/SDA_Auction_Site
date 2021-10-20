from django.urls import path
from .views import place_bid, buy_now, purchase_summary, purchased

app_name = 'bid_buy'

urlpatterns = [
    path('bid/<pk>', place_bid, name='place_bid'),
    path('buy/<pk>', buy_now, name='buy_now'),
    path('purchase/<bid_pk>', purchase_summary, name='auction_purchase'),
    path('purchased/', purchased, name='purchased'),
]
