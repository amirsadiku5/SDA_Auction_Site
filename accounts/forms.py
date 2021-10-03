from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ChoiceField, ImageField

from accounts.models import Account

TYPES = (
        ("NRM", "Normal Account"),
        ("PRM", "Premium Account")
    )


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    city = CharField(max_length=40)
    address = CharField(max_length=100)
    account_type = ChoiceField(choices=TYPES)
    avatar = ImageField()

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        city = self.cleaned_data['city']
        address = self.cleaned_data['address']
        account_type = self.cleaned_data['account_type']
        avatar = self.cleaned_data['avatar']
        account = Account(user=result, city=city, address=address, account_type=account_type, avatar=avatar)
        if commit:
            account.save()
        return super(SignUpForm, self).save(commit)
