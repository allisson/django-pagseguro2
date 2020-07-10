import json

from dateutil.parser import parse
from django.dispatch import Signal

from pagseguro.settings import TRANSACTION_STATUS

checkout_realizado = Signal(providing_args=["data"])
checkout_realizado_com_sucesso = Signal(providing_args=["data"])
checkout_realizado_com_erro = Signal(providing_args=["data"])

# API MODELO DE APLICAÇÕES
pedido_autorizacao_realizado = Signal(providing_args=["data"])
pedido_autorizacao_realizado_com_sucesso = Signal(providing_args=["data"])
pedido_autorizacao_realizado_com_erro = Signal(providing_args=["data"])

# API MODELO DE APLICAÇÕES
notificacao_autorizacao_recebida = Signal(providing_args=["authorization"])


notificacao_recebida = Signal(providing_args=["transaction"])
notificacao_status_aguardando = Signal(providing_args=["transaction"])
notificacao_status_em_analise = Signal(providing_args=["transaction"])
notificacao_status_pago = Signal(providing_args=["transaction"])
notificacao_status_disponivel = Signal(providing_args=["transaction"])
notificacao_status_em_disputa = Signal(providing_args=["transaction"])
notificacao_status_devolvido = Signal(providing_args=["transaction"])
notificacao_status_cancelado = Signal(providing_args=["transaction"])
notificacao_status_debitado = Signal(providing_args=["transaction"])
notificacao_status_retencao_temporaria = Signal(providing_args=["transaction"])


NOTIFICATION_STATUS = {
    "1": notificacao_status_aguardando,
    "2": notificacao_status_em_analise,
    "3": notificacao_status_pago,
    "4": notificacao_status_disponivel,
    "5": notificacao_status_em_disputa,
    "6": notificacao_status_devolvido,
    "7": notificacao_status_cancelado,
    "8": notificacao_status_debitado,
    "9": notificacao_status_retencao_temporaria,
}


def save_authorization(sender, authorization, **kwargs):
    """API MODELO DE APLICAÇÕES"""
    from pagseguro.models import Authorization

    try:
        authorization_app = Authorization.objects.get(code=authorization.get("code"))
    except Authorization.DoesNotExist:
        authorization_app = Authorization(
            code=authorization.get("code"),
            date=authorization.get("creationDate"),
            reference=authorization.get("reference"),
            authorizer_email=authorization.get("authorizerEmail"),
            public_key=authorization.get("account").get("publicKey"),
        )

    authorization_app.save()


def save_request_authorization(sender, data, **kwargs):
    """API MODELO DE APLICAÇÕES"""
    from pagseguro.models import RequestAuthorization

    authorization = RequestAuthorization(
        date=data.get("date"), success=data.get("success"), reference=data.get("reference")
    )

    if authorization.success:
        authorization.code = data.get("code")
    else:
        authorization.message = data.get("message")

    authorization.save()


def save_checkout(sender, data, **kwargs):
    from pagseguro.models import Checkout

    checkout = Checkout(date=data.get("date"), success=data.get("success"))

    if checkout.success:
        checkout.code = data.get("code")
    else:
        checkout.message = data.get("message")

    checkout.save()


def update_transaction(sender, transaction, **kwargs):
    from pagseguro.models import Transaction, TransactionHistory

    trans = transaction

    try:
        transaction = Transaction.objects.get(code=trans.get("code"))
    except Transaction.DoesNotExist:
        transaction = Transaction.objects.create(
            code=trans.get("code"),
            status=TRANSACTION_STATUS[trans.get("status")],
            date=parse(trans.get("date")),
            last_event_date=parse(trans.get("lastEventDate")),
            content=json.dumps(trans, indent=2),
            reference=trans.get("reference", ""),
        )

    transaction.status = TRANSACTION_STATUS[trans.get("status")]
    transaction.last_event_date = parse(trans.get("lastEventDate"))
    transaction.content = json.dumps(trans, indent=2)
    transaction.save()

    TransactionHistory.objects.create(
        transaction=transaction,
        status=TRANSACTION_STATUS[trans.get("status")],
        date=parse(trans.get("lastEventDate")),
    )
