from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from add_auction.forms import AuctionForm
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello")


# Create your views here.
class AddAuction(CreateView):
    template_name = "add_auction.html"
    form_class = AuctionForm
    success_url = reverse_lazy('user_auctions')
    permission_required = 'auction.add_auction'

    def form_valid(self, form):
        messages.success(request=self.request,
                         message="Auction has been added successfully!",
                         extra_tags="alert alert-success")
        return super(AddAuction, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,
                       message="Some of the given data are invalid!",
                       extra_tags="alert alert-danger")
        return super(AddAuction, self).form_invalid(form)
