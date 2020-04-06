import logging

import requests
import xmltodict
from dateutil.parser import parse
from django.utils import timezone

from pagseguro.forms import PagSeguroItemForm
from pagseguro.settings import (
    CHECKOUT_URL,
    NOTIFICATION_URL,
    PAGSEGURO_EMAIL,
    PAGSEGURO_TOKEN,
    PAYMENT_URL,
    SESSION_URL,
    TRANSACTION_URL,
)
from pagseguro.signals import (
    NOTIFICATION_STATUS,
    checkout_realizado,
    checkout_realizado_com_erro,
    checkout_realizado_com_sucesso,
    notificacao_recebida,
)

logger = logging.getLogger(__name__)


class PagSeguroItem(object):
    def __init__(
        self, id, description, amount, quantity, shipping_cost=None, weight=None, form_class=None,
    ):
        self.id = id
        self.description = description
        self.amount = amount
        self.quantity = quantity
        self.shipping_cost = shipping_cost
        self.weight = weight
        self.form_class = form_class or PagSeguroItemForm
        self.validate()

    def get_data(self):
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "quantity": self.quantity,
            "shipping_cost": self.shipping_cost,
            "weight": self.weight,
        }

    def validate(self):
        form = self.form_class(self.get_data())

        if form.is_valid():
            for k, v in form.cleaned_data.items():
                setattr(self, k, v)
        else:
            raise Exception(form.errors.items())

    def __repr__(self):
        return "<PagSeguroItem: {!r}>".format(self.get_data())


class PagSeguroApi(object):
    def __init__(
        self,
        checkout_url=None,
        redirect_url=None,
        notification_url=None,
        transaction_url=None,
        pagseguro_email=None,
        pagseguro_token=None,
        currency="BRL",
        **kwargs,
    ):
        self.checkout_url = checkout_url or CHECKOUT_URL
        self.redirect_url = redirect_url or PAYMENT_URL
        self.notification_url = notification_url or NOTIFICATION_URL
        self.transaction_url = transaction_url or TRANSACTION_URL
        self.pagseguro_email = pagseguro_email or PAGSEGURO_EMAIL
        self.pagseguro_token = pagseguro_token or PAGSEGURO_TOKEN
        self.currency = currency
        self.base_params = {
            "email": self.pagseguro_email,
            "token": self.pagseguro_token,
            "currency": self.currency,
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
            self.params["itemId{}".format(count)] = item.id
            self.params["itemDescription{}".format(count)] = item.description
            self.params["itemAmount{}".format(count)] = item.amount
            self.params["itemQuantity{}".format(count)] = item.quantity
            if item.shipping_cost:
                self.params["itemShippingCost{}".format(count)] = item.shipping_cost
            if item.weight:
                self.params["itemWeight{}".format(count)] = item.weight

    def checkout(self):
        self.build_params()
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        response = requests.post(self.checkout_url, self.params, headers=headers)

        data = {}

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            data = {
                "code": root["checkout"]["code"],
                "status_code": response.status_code,
                "date": parse(root["checkout"]["date"]),
                "redirect_url": "{}?code={}".format(self.redirect_url, root["checkout"]["code"]),
                "success": True,
            }
            checkout_realizado_com_sucesso.send(sender=self, data=data)
        else:
            data = {
                "status_code": response.status_code,
                "message": response.text,
                "success": False,
                "date": timezone.now(),
            }
            checkout_realizado_com_erro.send(sender=self, data=data)

        checkout_realizado.send(sender=self, data=data)

        logger.debug("operation=api_checkout, data={!r}".format(data))
        return data

    def get_notification(self, notification_id):
        response = requests.get(
            self.notification_url + "/{}".format(notification_id),
            params={"email": self.base_params["email"], "token": self.base_params["token"]},
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root["transaction"]
            notificacao_recebida.send(sender=self, transaction=transaction)

            status = transaction["status"]
            if status in NOTIFICATION_STATUS:
                signal = NOTIFICATION_STATUS[status]
                signal.send(sender=self, transaction=transaction)

        logger.debug(
            "operation=api_get_notification, "
            "notification_id={}, "
            "response_body={}, "
            "response_status={}".format(notification_id, response.text, response.status_code)
        )
        return response

    def get_transaction(self, transaction_id):
        response = requests.get(
            self.transaction_url + "/{}".format(transaction_id),
            params={"email": self.base_params["email"], "token": self.base_params["token"]},
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root["transaction"]

            data = {
                "transaction": transaction,
                "status_code": response.status_code,
                "success": True,
                "date": timezone.now(),
            }
        else:
            data = {
                "status_code": response.status_code,
                "message": response.text,
                "success": False,
                "date": timezone.now(),
            }

        logger.debug(
            "operation=api_get_transaction, "
            "transaction_id={}, "
            "data={!r}, "
            "response_status={}".format(transaction_id, data, response.status_code)
        )
        return data


class PagSeguroApiTransparent(PagSeguroApi):
    def __init__(self, session_url=None, **kwargs):
        self.session_url = session_url or SESSION_URL
        super(PagSeguroApiTransparent, self).__init__(**kwargs)
        self.base_params["paymentMode"] = "default"

    def set_sender_hash(self, hash_code):
        self.params["senderHash"] = hash_code

    def set_receiver_email(self, email):
        self.params["receiverEmail"] = email

    def set_payment_method(self, method):
        self.params["paymentMethod"] = method

    def set_extra_amount(self, amount):
        self.params["extraAmount"] = amount

    def set_notification_url(self, url):
        self.params["notificationURL"] = url

    def set_bank_name(self, name):
        self.params["bankName"] = name

    def set_sender(self, name, area_code, phone, email, cpf, cnpj=None, born_date=None):
        self.params["senderName"] = name
        self.params["senderAreaCode"] = area_code
        self.params["senderPhone"] = phone
        self.params["senderEmail"] = email
        self.params["senderCPF"] = cpf
        self.params["senderCNPJ"] = cnpj
        self.params["senderBornDate"] = born_date

    def set_shipping(
        self,
        street,
        number,
        complement,
        district,
        postal_code,
        city,
        state,
        country,
        cost=None,
        shipping_type=None,
    ):
        self.params["shippingAddressStreet"] = street
        self.params["shippingAddressNumber"] = number
        self.params["shippingAddressComplement"] = complement
        self.params["shippingAddressDistrict"] = district
        self.params["shippingAddressPostalCode"] = postal_code
        self.params["shippingAddressCity"] = city
        self.params["shippingAddressState"] = state
        self.params["shippingAddressCountry"] = country
        self.params["shippingCost"] = cost
        self.params["shippingType"] = shipping_type

    def set_creditcard_data(
        self, quantity, value, name, birth_date, cpf, area_code, phone, no_interest_quantity=None,
    ):
        self.params["installmentQuantity"] = quantity
        self.params["installmentValue"] = value
        self.params["creditCardHolderName"] = name
        self.params["creditCardHolderBirthDate"] = birth_date
        self.params["creditCardHolderCPF"] = cpf
        self.params["creditCardHolderAreaCode"] = area_code
        self.params["creditCardHolderPhone"] = phone
        if no_interest_quantity:
            self.params["noInterestInstallmentQuantity"] = no_interest_quantity

    def set_creditcard_billing_address(
        self, street, number, district, postal_code, city, state, country, complement=None,
    ):
        self.params["billingAddressStreet"] = street
        self.params["billingAddressNumber"] = number
        self.params["billingAddressDistrict"] = district
        self.params["billingAddressPostalCode"] = postal_code
        self.params["billingAddressCity"] = city
        self.params["billingAddressState"] = state
        self.params["billingAddressCountry"] = country
        self.params["billingAddressComplement"] = complement

    def set_creditcard_token(self, token):
        self.params["creditCardToken"] = token

    def checkout(self):
        self.build_params()
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        response = requests.post(self.transaction_url, self.params, headers=headers)

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            transaction = root["transaction"]
            data = {
                "transaction": transaction,
                "status_code": response.status_code,
                "success": True,
                "date": parse(transaction["date"]),
                "code": transaction["code"],
            }
            checkout_realizado_com_sucesso.send(sender=self, data=data)
        else:
            data = {
                "status_code": response.status_code,
                "message": response.text,
                "success": False,
                "date": timezone.now(),
            }
            checkout_realizado_com_erro.send(sender=self, data=data)

        checkout_realizado.send(sender=self, data=data)

        logger.debug("operation=transparent_api_checkout, " "data={!r}".format(data))
        return data

    def get_session_id(self):
        response = requests.post(
            self.session_url, params={"email": self.base_params["email"], "token": self.base_params["token"]},
        )

        if response.status_code == 200:
            root = xmltodict.parse(response.text)
            session_id = root["session"]["id"]
            data = {
                "session_id": session_id,
                "status_code": response.status_code,
                "success": True,
                "date": timezone.now(),
            }
        else:
            data = {
                "status_code": response.status_code,
                "message": response.text,
                "success": False,
                "date": timezone.now(),
            }

        logger.debug("operation=transparent_api_get_session_id, " "data={!r}".format(data))
        return data
