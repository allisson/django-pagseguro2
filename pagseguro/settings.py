from django.conf import settings

PAGSEGURO_EMAIL = getattr(settings, "PAGSEGURO_EMAIL", "")
PAGSEGURO_TOKEN = getattr(settings, "PAGSEGURO_TOKEN", "")
PAGSEGURO_SANDBOX = getattr(settings, "PAGSEGURO_SANDBOX", True)
PAGSEGURO_LOG_IN_MODEL = getattr(settings, "PAGSEGURO_LOG_IN_MODEL", True)
# API MODELO DE APLICAÇÕES
PAGSEGURO_APP_KEY = getattr(settings, "PAGSEGURO_APP_KEY", "")
PAGSEGURO_APP_ID = getattr(settings, "PAGSEGURO_APP_ID", "")
PAGSEGURO_AUTHORIZATIONS_RETURN = getattr(settings, "PAGSEGURO_AUTHORIZATIONS_RETURN", "http://seusite.com.br/redirect")

if PAGSEGURO_SANDBOX:
    CHECKOUT_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/checkout"
    PAYMENT_URL = "https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html"
    NOTIFICATION_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/transactions/notifications"
    TRANSACTION_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/transactions"
    SESSION_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/sessions/"
    # API MODELO DE APLICAÇÕES - AUTORIZAÇÕES
    REQUESTING_AUTHORIZATIONS_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/authorizations/request/"
    REDIRECT_AUTHORIZATIONS_URL = "https://sandbox.pagseguro.uol.com.br/v2/authorization/request.jhtml"
    AUTHORIZATIONS_URL = "https://ws.sandbox.pagseguro.uol.com.br/v2/authorizations/notifications"
else:
    CHECKOUT_URL = "https://ws.pagseguro.uol.com.br/v2/checkout"
    PAYMENT_URL = "https://pagseguro.uol.com.br/v2/checkout/payment.html"
    NOTIFICATION_URL = "https://ws.pagseguro.uol.com.br/v2/transactions/notifications"
    TRANSACTION_URL = "https://ws.pagseguro.uol.com.br/v2/transactions"
    SESSION_URL = "https://ws.pagseguro.uol.com.br/v2/sessions/"
    # API MODELO DE APLICAÇÕES - AUTORIZAÇÕES
    REQUESTING_AUTHORIZATIONS_URL = "https://ws.pagseguro.uol.com.br/v2/authorizations/request/"
    REDIRECT_AUTHORIZATIONS_URL = "https://pagseguro.uol.com.br/v2/authorization/request.jhtml"
    AUTHORIZATIONS_URL = "https://ws.pagseguro.uol.com.br/v2/authorizations/notifications"

TRANSACTION_STATUS = {
    "1": "aguardando",
    "2": "em_analise",
    "3": "pago",
    "4": "disponivel",
    "5": "em_disputa",
    "6": "devolvido",
    "7": "cancelado",
    "8": "debitado",
    "9": "retencao_temporaria",
}
