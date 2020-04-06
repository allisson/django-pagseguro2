from decimal import Decimal

from django import forms


class PagSeguroItemForm(forms.Form):
    id = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    amount = forms.DecimalField(
        max_digits=9, max_value=Decimal("9999999.00"), min_value=Decimal("0.01"), decimal_places=2,
    )
    quantity = forms.IntegerField(min_value=1, max_value=999)
    shipping_cost = forms.DecimalField(
        max_digits=9,
        max_value=Decimal("9999999.00"),
        min_value=Decimal("0.01"),
        decimal_places=2,
        required=False,
    )
    weight = forms.IntegerField(min_value=1, max_value=30000, required=False)

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount:
            exponent = abs(amount.as_tuple().exponent)

            if exponent != 2:
                raise forms.ValidationError("O amount deve conter duas casas decimais.")

        return amount

    def clean_shipping_cost(self):
        shipping_cost = self.cleaned_data.get("shipping_cost")

        if shipping_cost:
            exponent = abs(shipping_cost.as_tuple().exponent)

            if exponent != 2:
                raise forms.ValidationError("O shipping_cost deve conter duas casas decimais.")

        return shipping_cost
