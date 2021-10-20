from django.forms import Form, DecimalField


class BidForm(Form):
    amount = DecimalField(min_value=1, decimal_places=2)
