#-*- coding: utf-8 -*-
import requests
import xmltodict
from dateutil.parser import parse
from datetime import datetime

from pagseguro.settings import (
    PAGSEGURO_EMAIL, PAGSEGURO_TOKEN, CHECKOUT_URL, PAYMENT_URL,
    NOTIFICATION_URL
)
from pagseguro.signals import (
    notificacao_recebida, NOTIFICATION_STATUS, checkout_realizado,
    checkout_realizado_com_sucesso, checkout_realizado_com_erro
)
from pagseguro.forms import PagSeguroItemForm


class PagSeguroItem(object):

    form_class = PagSeguroItemForm
    id = None
    description = None
    amount = None
    quantity = None
    shipping_cost = None
    weight = None

    def __init__(self, id, description, amount, quantity, shipping_cost=None,
                 weight=None):
        form_data = {
            'id': id,
            'description': description,
            'amount': amount,
            'quantity': quantity,
            'shipping_cost': shipping_cost,
            'weight': weight
        }
        form = self.form_class(form_data)

        if form.is_valid():
            for k, v in form.cleaned_data.items():
                setattr(self, k, v)
        else:
            raise Exception(form.errors.items())

    def __repr__(self):
        return '<PagSeguroItem: {0}>'.format(self.description)


class PagSeguroApi(object):

    checkout_url = CHECKOUT_URL
    redirect_url = PAYMENT_URL
    notification_url = NOTIFICATION_URL

    itens = []
    base_params = {
        'email': PAGSEGURO_EMAIL,
        'token': PAGSEGURO_TOKEN,
        'currency': 'BRL',
    }
    params = {}

    def __init__(self, **kwargs):
        self.base_params.update(kwargs)

    def add_item(self, item):
        self.itens.append(item)

    def get_items(self):
        return self.itens

    def clear_items(self):
        self.itens = []

    def build_params(self):
        self.params = {}
        self.params.update(self.base_params)

        for index, item in enumerate(self.itens):
            count = index + 1
            self.params['itemId{0}'.format(count)] = item.id
            self.params['itemDescription{0}'.format(count)] = item.description
            self.params['itemAmount{0}'.format(count)] = item.amount
            self.params['itemQuantity{0}'.format(count)] = item.quantity
            if item.shipping_cost:
                self.params['itemShippingCost{0}'.format(count)] = item.shipping_cost
            if item.weight:
                self.params['itemWeight{0}'.format(count)] = item.weight

    def checkout(self):
        self.build_params()
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response = requests.post(
            self.checkout_url, self.params, headers=headers
        )

        data = {}

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            data = {
                'code': root['checkout']['code'],
                'status_code': response.status_code,
                'date': parse(root['checkout']['date']),
                'redirect_url': '{0}?code={1}'.format(
                    self.redirect_url, root['checkout']['code']
                ),
                'success': True
            }
            checkout_realizado_com_sucesso.send(
                sender=self, data=data
            )
        else:
            data = {
                'status_code': response.status_code,
                'message': response.text,
                'success': False,
                'date': datetime.now()
            }
            checkout_realizado_com_erro.send(
                sender=self, data=data
            )

        checkout_realizado.send(
            sender=self, data=data
        )

        return data

    def get_notification(self, notification_id):
        response = requests.get(
            self.notification_url + '/{0}'.format(notification_id),
            params={
                'email': self.base_params['email'],
                'token': self.base_params['token']
            }
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root['transaction']
            notificacao_recebida.send(
                sender=self, transaction=transaction
            )

            status = transaction['status']
            if status in NOTIFICATION_STATUS:
                signal = NOTIFICATION_STATUS[status]
                signal.send(
                    sender=self, transaction=transaction
                )

        return response
