from django.urls import path
from auctions.views import AuctionCategoryListView, AuctionListView, AuctionDetailView

app_name = 'auctions'

urlpatterns = [
    path('categorylist/', AuctionCategoryListView.as_view(), name='categories_list'),
    path('auction-list/<category_pk>', AuctionListView.as_view(), name='auctions'),
    path('details/<pk>', AuctionDetailView.as_view(), name='auction_details'),
]