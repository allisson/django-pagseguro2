# -*- coding: utf-8 -*-
from django import forms


class PagSeguroItemForm(forms.Form):

    id = forms.CharField(
        max_length=100
    )

    description = forms.CharField(
        max_length=100
    )

    amount = forms.DecimalField(
        max_digits=9,
        max_value=9999999,
        min_value=1,
        decimal_places=2
    )

    quantity = forms.IntegerField(
        min_value=1,
        max_value=999
    )

    shipping_cost = forms.DecimalField(
        max_digits=9,
        max_value=9999999,
        min_value=1,
        decimal_places=2,
        required=False
    )

    weight = forms.IntegerField(
        min_value=1,
        max_value=30000,
        required=False
    )
