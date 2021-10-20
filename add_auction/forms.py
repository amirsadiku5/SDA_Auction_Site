from django.forms import Form, CharField, IntegerField, DateField, Textarea, ModelChoiceField, ModelForm
from django.core.exceptions import ValidationError
from datetime import date
import re

from auctions.models import Auction


def capitalize_validator(value):
    if value[0].islower():
        raise ValidationError("Value should be capitalized!")


class PastDateField(DateField):
    def validate(self, value):
        super(PastDateField, self).validate(value)
        if value > date.today():
            raise ValidationError("Past dates required!")

    def clean(self, value):
        result = super(PastDateField, self).clean(value)
        return date(year=result.year, month=result.month, day=1)


# MovieForm inherits Form
# class MovieForm(Form):
#     title = CharField(max_length=128, validators=[capitalize_validator])
#     rating = IntegerField(min_value=1, max_value=10)
#     released = PastDateField()
#     genre = ModelChoiceField(queryset=Genre.objects)
#     description = CharField(widget=Textarea, required=False)

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ('auction_status', 'owner', 'visits_number')

    def clean_description(self):
        # Start with capital letter
        initial = self.cleaned_data["description"]
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

