#-*- coding: utf-8 -*-
from django.dispatch import Signal

from dateutil.parser import parse
import json

from pagseguro.settings import TRANSACTION_STATUS


checkout_realizado = Signal(providing_args=['data'])
checkout_realizado_com_sucesso = Signal(providing_args=['data'])
checkout_realizado_com_erro = Signal(providing_args=['data'])

notificacao_recebida = Signal(providing_args=['transaction'])
notificacao_status_aguardando = Signal(providing_args=['transaction'])
notificacao_status_em_analise = Signal(providing_args=['transaction'])
notificacao_status_pago = Signal(providing_args=['transaction'])
notificacao_status_disponivel = Signal(providing_args=['transaction'])
notificacao_status_em_disputa = Signal(providing_args=['transaction'])
notificacao_status_devolvido = Signal(providing_args=['transaction'])
notificacao_status_cancelado = Signal(providing_args=['transaction'])


NOTIFICATION_STATUS = {
    '1': notificacao_status_aguardando,
    '2': notificacao_status_em_analise,
    '3': notificacao_status_pago,
    '4': notificacao_status_disponivel,
    '5': notificacao_status_em_disputa,
    '6': notificacao_status_devolvido,
    '7': notificacao_status_cancelado
}


def save_checkout(sender, data, **kwargs):
    from pagseguro.models import Checkout

    checkout = Checkout(
        date=data['date'],
        success=data['success']
    )

    if checkout.success:
        checkout.code = data['code']
    else:
        checkout.message = data['message']

    checkout.save()


def update_transaction(sender, transaction, **kwargs):
    from pagseguro.models import Transaction, TransactionHistory

    trans = transaction

    try:
        transaction = Transaction.objects.get(code=trans['code'])
    except Transaction.DoesNotExist:
        transaction = Transaction(
            code=trans['code'],
            status=TRANSACTION_STATUS[trans['status']],
            date=parse(trans['date']),
            last_event_date=parse(trans['lastEventDate']),
            content=json.dumps(trans, indent=2)
        )

        if 'reference' in trans:
            transaction.reference = trans['reference']

        transaction.save()

    transaction.status = TRANSACTION_STATUS[trans['status']]
    transaction.last_event_date = parse(trans['lastEventDate'])
    transaction.content = json.dumps(trans, indent=2)
    transaction.save()

    TransactionHistory.objects.create(
        transaction=transaction,
        status=TRANSACTION_STATUS[trans['status']],
        date=parse(trans['lastEventDate'])
    )
