from django import forms

subscription_options = [
    ("Once", "One Time Donation"),
    ("1-month", "1-Month subscription ($10 USD/Mon)"),
    ("6-month", "6-Month subscription Save $10 ($50 USD/Mon)"),
    ("1-year", "1-Year subscription Save $30 ($90 USD/Mon)"),
]


class DonationForm(forms.Form):
    amount = forms.IntegerField()
    plans = forms.ChoiceField(choices=subscription_options)
    purpose = forms.CharField(
        widget=forms.Textarea(attrs={"name": "purpose", "rows": 3, "cols": 5})
    )
