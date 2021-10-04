from django.shortcuts import render
from django.views.generic import ListView, DetailView
from auctions.models import AuctionCategory, Auction


class AuctionCategoryListView(ListView):
    model = AuctionCategory
    template_name = 'auctions/auction_categories.html'


class AuctionListView(ListView):
    model = Auction
    template_name = 'auctions/items.html'

    def get_queryset(self):
        category_pk = self.kwargs["category_pk"]
        chosen_category = AuctionCategory.objects.get(pk=category_pk)
        queryset = Auction.objects.filter(category=chosen_category)
        return queryset


class AuctionDetailView(DetailView):
    model = Auction
    template_name = 'auctions/item_details.html'
