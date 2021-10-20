from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import Account
from auctions.models import Auction
from .models import Bid, Purchase
from .forms import BidForm


@login_required
def place_bid(request, pk):
    item = Auction.objects.get(pk=pk)
    bids = Bid.objects.filter(item=item).order_by("-amount_to_pay")
    if len(bids) == 0:
        highest_bid = 0
        highest_bidder = None
    else:
        highest_bid = bids[0].amount_to_pay
        highest_bidder = bids[0].bidder

    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            placed_bid = bid_form.cleaned_data["amount"]
            if placed_bid > request.user.account.credit:
                messages.error(request=request,
                               message="Your credit is insufficient!",
                               extra_tags="alert alert-danger")
            elif placed_bid < item.minimal_price:
                messages.error(request=request,
                               message="Your bid is lower than the minimal price",
                               extra_tags="alert alert-danger")
            elif placed_bid >= item.buy_now_price:
                messages.error(request=request,
                               message="Your bid is higher than the buy now price. Consider buying the item directly",
                               extra_tags="alert alert-danger")
            elif placed_bid > highest_bid:
                Bid.objects.create(item=item, bidder=request.user.account, amount_to_pay=placed_bid)
                request.user.account.credit = request.user.account.credit - placed_bid
                request.user.account.save()
                if highest_bidder:
                    highest_bidder.credit += highest_bid
                    highest_bidder.save()
                messages.success(request=request,
                                 message=f"Bid {placed_bid} placed successfully!",
                                 extra_tags="alert alert-success")
            else:
                messages.error(request=request,
                               message="Your bid is lower than the current highest bid",
                               extra_tags="alert alert-danger")
        else:
            messages.error(request=request,
                           message="Invalid bid",
                           extra_tags="alert alert-danger")

    return redirect("auctions:auction_details", pk=pk)


@login_required
def buy_now(request, pk):
    item = Auction.objects.get(pk=pk)
    bids = Bid.objects.filter(item=item).order_by("-amount_to_pay")
    if len(bids) == 0:
        highest_bid = 0
        highest_bidder = None
    else:
        highest_bid = bids[0].amount_to_pay
        highest_bidder = bids[0].bidder

    if item.buy_now_price > request.user.account.credit:
        messages.error(request=request,
                       message="Your credit is insufficient!",
                       extra_tags="alert alert-danger")
    else:
        if item.auction_status != "PUR":
            item.auction_status = "PUR"
            item.save()
            purchase = Bid.objects.create(item=item, bidder=request.user.account,
                                          amount_to_pay=item.buy_now_price, bid_type="BYN")
            request.user.account.credit = request.user.account.credit - item.buy_now_price
            request.user.account.save()

            Purchase.objects.create(bid=purchase)

            item.owner.credit += item.buy_now_price
            item.owner.save()

            if highest_bidder:
                highest_bidder.credit += highest_bid
                highest_bidder.save()
            messages.success(request=request,
                             message=f"The item has been purchased successfully!",
                             extra_tags="alert alert-success")

            return redirect("bid_buy:auction_purchase", bid_pk=purchase.pk)
        else:
            messages.error(request=request,
                           message="Item is already purchased",
                           extra_tags="alert alert-danger")

    return redirect("auctions:auction_details", pk=pk)


# @permission_required
@login_required
def purchase_summary(request, bid_pk):
    bid = Bid.objects.get(pk=bid_pk)
    auction = bid.item
    purchase_price = bid.amount_to_pay

    return render(request, template_name="bid_buy/auction_purchase.html",
                  context={"auction": auction, "purchase_price": purchase_price})


@login_required
def purchased(request):
    if not Account.objects.filter(user=request.user).exists():
        return redirect('accounts:logout')
    account = Account.objects.get(user=request.user)
    purchases = Purchase.objects.all()
    user_purchases = []
    for purchase in purchases:
        if purchase.bid.bidder == account:
            user_purchases.append(purchase)

    return render(request, template_name='bid_buy/purchased.html',
                  context={"purchases": user_purchases})
