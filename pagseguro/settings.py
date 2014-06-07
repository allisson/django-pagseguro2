#-*- coding: utf-8 -*-
from django.conf import settings

PAGSEGURO_EMAIL = getattr(settings, 'PAGSEGURO_EMAIL', '')
PAGSEGURO_TOKEN = getattr(settings, 'PAGSEGURO_TOKEN', '')
PAGSEGURO_SANDBOX = getattr(settings, 'PAGSEGURO_SANDBOX', True)

if PAGSEGURO_SANDBOX:
    CHECKOUT_URL = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout'
    PAYMENT_URL = 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html'
    NOTIFICATION_URL = 'https://ws.sandbox.pagseguro.uol.com.br/v2/transactions/notifications'
else:
    CHECKOUT_URL = 'https://ws.pagseguro.uol.com.br/v2/checkout'
    PAYMENT_URL = 'https://pagseguro.uol.com.br/v2/checkout/payment.html'
    NOTIFICATION_URL = 'https://ws.pagseguro.uol.com.br/v2/transactions/notifications'
