from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import OneToOneField, Model, CASCADE, ImageField, CharField, DateField, DecimalField


class Account(Model):
    # email used for communication and notifications
    user = OneToOneField(User, on_delete=CASCADE)
    # username to be presented on the account profile
    city = CharField(max_length=128)
    # street, home number, ZIP code
    address = CharField(max_length=128)
    account_creation_date = DateField(auto_now_add=True)
    # active/inactive/blocked accounts
    STATUSES = (
        ("ACT", "Active"),
        ("INA", "Inactive"),
        ("BLC", "Blocked")
    )
    account_status = CharField(
        max_length=3,
        choices=STATUSES,
        default="INA"
    )
    # normal/premium accounts
    TYPES = (
        ("NRM", "Normal Account"),
        ("PRM", "Premium Account")
    )
    account_type = CharField(
        max_length=3,
        choices=TYPES,
        default="NRM"
    )
    avatar = ImageField(upload_to="images/")
    credit = DecimalField(max_digits=8, decimal_places=2, default=100)

    def __str__(self):
        return f"{self.user} Profile-{self.pk}={self.user.pk}"
