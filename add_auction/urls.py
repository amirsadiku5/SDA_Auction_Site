from django.urls import path
from add_auction.views import AddAuction, hello

app_name = 'add_auction'

urlpatterns = [
    path('', AddAuction.as_view(), name='add_auction'),
]
