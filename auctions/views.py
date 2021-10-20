import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from accounts.models import Account
from auctions.models import AuctionCategory, Auction
from bid_buy.forms import BidForm
from bid_buy.models import Bid, Purchase


class AuctionCategoryListView(ListView):
    model = AuctionCategory
    template_name = 'auctions/auction_categories.html'


class AuctionListView(ListView):
    model = Auction
    template_name = 'auctions/items.html'

    def get_queryset(self):
        category_pk = self.kwargs["category_pk"]
        chosen_category = AuctionCategory.objects.get(pk=category_pk)
        queryset = Auction.objects.filter(category=chosen_category).filter(auction_status="STA")
        return queryset


class AuctionDetailView(DetailView):
    model = Auction
    template_name = 'auctions/item_details.html'
    extra_context = {"bid_form": BidForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_pk = self.kwargs["pk"]
        item = Auction.objects.get(pk=item_pk)
        item.visits_number += 1
        item.save()
        bids = Bid.objects.filter(item=item).order_by("-amount_to_pay")
        if len(bids) == 0:
            highest_bid = 0
        else:
            highest_bid = bids[0].amount_to_pay

        context['highest_bid'] = highest_bid

        return context

    def get(self, request, *args, **kwargs):
        item_pk = self.kwargs["pk"]
        item = Auction.objects.get(pk=item_pk)
        if item.auction_status == "STA" and item.auction_end < timezone.now():
            bids = Bid.objects.filter(item=item).order_by("-amount_to_pay")
            if len(bids) == 0:
                item.auction_status = "EXP"
                item.save()
            else:
                highest_bid = bids[0].amount_to_pay
                if item.auction_status != "PUR":
                    item.auction_status = "PUR"
                    item.save()

                    item.owner.credit += highest_bid
                    item.owner.save()

                    Purchase.objects.create(bid=bids[0])

                    messages.success(request=request,
                                     message=f"{bids[0].bidder} just won the item {item.title} at price "
                                             f"of {bids[0].amount_to_pay} credits!",
                                     extra_tags="alert alert-success")

        return super().get(request, *args, **kwargs)


def user_auctions(request):
    if not Account.objects.filter(user=request.user).exists():
        return redirect('accounts:logout')
    account = Account.objects.get(user=request.user)
    auctions = Auction.objects.filter(owner=account)
    return render(request, template_name='auctions/user_items.html', context={"auctions": auctions})
