from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from accounts.models import Account
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


def user_auctions(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if not Account.objects.filter(user=user).exists():
        return redirect('accounts:logout')
    account = Account.objects.get(user=user)
    auctions = Auction.objects.filter(owner=account)
    return render(request, template_name='auctions/user_items.html', context={"auctions": auctions})
