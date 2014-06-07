#-*- coding: utf-8 -*-
from django.dispatch import Signal


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
