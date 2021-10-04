from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView
# from accounts.forms import SignUpForm
from accounts.forms import SignUpForm
from accounts.models import Account


class CustomLoginView(LoginView):
    template_name = 'form.html'
    success_url = reverse_lazy('auctions')

    def form_valid(self, form):
        messages.success(self.request,
                         "Login successful",
                         extra_tags="alert alert-success")
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = 'auctions.html'


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/profile_view.html'

    def get(self, request, *args, **kwargs):
        if Account.objects.filter(user=self.request.user).exists():
            self.extra_context = {"account": Account.objects.get(user=self.request.user)}
            return super().get(request, *args, **kwargs)
        else:
            return redirect('accounts:logout')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('auctions')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message="Password changed successfully!",
                         extra_tags="alert alert-success")
        return super(ChangePasswordView, self).form_valid(form)
