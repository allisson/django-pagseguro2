# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
import requests
import xmltodict
from dateutil.parser import parse

from pagseguro.settings import (
    PAGSEGURO_EMAIL, PAGSEGURO_TOKEN, CHECKOUT_URL, PAYMENT_URL,
    NOTIFICATION_URL, TRANSACTION_URL, SESSION_URL
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
    transaction_url = TRANSACTION_URL

    def __init__(self, **kwargs):
        self.base_params = {
            'email': PAGSEGURO_EMAIL,
            'token': PAGSEGURO_TOKEN,
            'currency': 'BRL',
        }
        self.base_params.update(kwargs)

        self.params = {}
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    def clear_items(self):
        self.items = []

    def build_params(self):
        self.params.update(self.base_params)

        for index, item in enumerate(self.items):
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
                'date': timezone.now()
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

    def get_transaction(self, transaction_id):
        response = requests.get(
            self.transaction_url + '/{0}'.format(transaction_id),
            params={
                'email': self.base_params['email'],
                'token': self.base_params['token']
            }
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root['transaction']

            data = {
                'transaction': transaction,
                'status_code': response.status_code,
                'success': True,
                'date': timezone.now()
            }
        else:
            data = {
                'status_code': response.status_code,
                'message': response.text,
                'success': False,
                'date': timezone.now()
            }

        return data


class PagSeguroApiTransparent(PagSeguroApi):

    session_url = SESSION_URL

    def __init__(self, **kwargs):
        super(PagSeguroApiTransparent, self).__init__(**kwargs)
        self.base_params['paymentMode'] = 'default'

    def set_sender_hash(self, hash_code):
        self.params['senderHash'] = hash_code

    def set_receiver_email(self, email):
        self.params['receiverEmail'] = email

    def set_payment_method(self, method):
        self.params['paymentMethod'] = method

    def set_extra_amount(self, amount):
        self.params['extraAmount'] = amount

    def set_notification_url(self, url):
        self.params['notificationURL'] = url

    def set_bank_name(self, name):
        self.params['bankName'] = name

    def set_sender(self, name, area_code, phone, email,
                   cpf, cnpj=None, born_date=None):
        self.params['senderName'] = name
        self.params['senderAreaCode'] = area_code
        self.params['senderPhone'] = phone
        self.params['senderEmail'] = email
        self.params['senderCPF'] = cpf
        self.params['senderCNPJ'] = cnpj
        self.params['senderBornDate'] = born_date

    def set_shipping(self, street, number, complement, district,
                     postal_code, city, state, country, cost=None,
                     shipping_type=None):
        self.params['shippingAddressStreet'] = street
        self.params['shippingAddressNumber'] = number
        self.params['shippingAddressComplement'] = complement
        self.params['shippingAddressDistrict'] = district
        self.params['shippingAddressPostalCode'] = postal_code
        self.params['shippingAddressCity'] = city
        self.params['shippingAddressState'] = state
        self.params['shippingAddressCountry'] = country
        self.params['shippingCost'] = cost
        self.params['shippingType'] = shipping_type

    def set_creditcard_data(self, quantity, value, name, birth_date,
                            cpf, area_code, phone):
        self.params['installmentQuantity'] = quantity
        self.params['installmentValue'] = value
        self.params['creditCardHolderName'] = name
        self.params['creditCardHolderBirthDate'] = birth_date
        self.params['creditCardHolderCPF'] = cpf
        self.params['creditCardHolderAreaCode'] = area_code
        self.params['creditCardHolderPhone'] = phone

    def set_creditcard_billing_address(self, street, number, district,
                                       postal_code, city, state, country,
                                       complement=None):
        self.params['billingAddressStreet'] = street
        self.params['billingAddressNumber'] = number
        self.params['billingAddressDistrict'] = district
        self.params['billingAddressPostalCode'] = postal_code
        self.params['billingAddressCity'] = city
        self.params['billingAddressState'] = state
        self.params['billingAddressCountry'] = country
        self.params['billingAddressComplement'] = complement

    def set_creditcard_token(self, token):
        self.params['creditCardToken'] = token

    def checkout(self):
        self.build_params()
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response = requests.post(
            self.transaction_url, self.params, headers=headers
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root['transaction']
            data = {
                'transaction': transaction,
                'status_code': response.status_code,
                'success': True,
                'date': parse(transaction['date']),
                'code': transaction['code'],
            }
            checkout_realizado_com_sucesso.send(
                sender=self, data=data
            )
        else:
            data = {
                'status_code': response.status_code,
                'message': response.text,
                'success': False,
                'date': timezone.now()
            }
            checkout_realizado_com_erro.send(
                sender=self, data=data
            )

        checkout_realizado.send(
            sender=self, data=data
        )

        return data

    def get_session_id(self):
        response = requests.post(
            self.session_url,
            params={
                'email': self.base_params['email'],
                'token': self.base_params['token']
            }
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            session_id = root['session']['id']
            data = {
                'session_id': session_id,
                'status_code': response.status_code,
                'success': True,
                'date': timezone.now()

            }
        else:
            data = {
                'status_code': response.status_code,
                'message': response.text,
                'success': False,
                'date': timezone.now()

            }

        return data
