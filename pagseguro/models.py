from django.db import models

from pagseguro.settings import PAGSEGURO_LOG_IN_MODEL
from pagseguro.signals import (
    checkout_realizado, notificacao_recebida, save_checkout, update_transaction,
    # API MODELO DE APLICAÇÕES
    pedido_autorizacao_realizado, notificacao_autorizacao_recebida, save_request_authorization, save_authorization)

TRANSACTION_STATUS_CHOICES = (
    ("aguardando", "Aguardando"),
    ("em_analise", "Em análise"),
    ("pago", "Pago"),
    ("disponivel", "Disponível"),
    ("em_disputa", "Em disputa"),
    ("devolvido", "Devolvido"),
    ("cancelado", "Cancelado"),
)


class Authorization(models.Model):
    code = models.CharField(
        "código da requisição", max_length=100, blank=True, help_text="Código gerado para redirecionamento.",
    )
    date = models.DateTimeField("Data", help_text="Data da solicitação.")

    reference = models.CharField(
        "referencia", unique=True, max_length=100, blank=True, help_text="Código único para controle",
    )

    authorizer_email = models.EmailField("Email do autorizador", help_text="Email de quem autorizou")

    public_key = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.pk)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Autorização"
        verbose_name_plural = "Autorizações"


class RequestAuthorization(models.Model):
    """
    Solicita autorização para gerenciar a conta de um vendedor
    """
    code = models.CharField(
        "código", max_length=100, blank=True, help_text="Código gerado para redirecionamento.",
    )
    date = models.DateTimeField("Data", help_text="Data em que a autorização foi solicitada.")
    success = models.BooleanField(
        "Sucesso", db_index=True, help_text="A solicitação de autorização foi feita com sucesso?", default=False,
    )
    message = models.TextField(
        "Mensagem de erro", blank=True, help_text="Mensagem apresentada no caso de erro na solicitação.",
    )

    reference = models.CharField(
        "referencia", unique=True, max_length=100, blank=True, help_text="Código único para controle",
    )

    def __str__(self):
        return "{0}".format(self.pk)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Solicitação de Autorização"
        verbose_name_plural = "Solicitações de Autorização"


class Checkout(models.Model):
    code = models.CharField(
        "código", max_length=100, blank=True, help_text="Código gerado para redirecionamento.",
    )
    date = models.DateTimeField("Data", help_text="Data em que o checkout foi realizado.")
    success = models.BooleanField(
        "Sucesso", db_index=True, help_text="O checkout foi feito com sucesso?", default=False,
    )
    message = models.TextField(
        "Mensagem de erro", blank=True, help_text="Mensagem apresentada no caso de erro no checkout.",
    )

    def __str__(self):
        return "{0}".format(self.pk)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Checkout"
        verbose_name_plural = "Checkouts"


class Transaction(models.Model):
    code = models.CharField(
        "código", max_length=100, unique=True, db_index=True, help_text="O código da transação.",
    )
    reference = models.CharField(
        "referência",
        max_length=200,
        db_index=True,
        blank=True,
        help_text="A referência passada na transação.",
    )
    status = models.CharField(
        "Status",
        max_length=20,
        db_index=True,
        choices=TRANSACTION_STATUS_CHOICES,
        help_text="Status atual da transação.",
    )
    date = models.DateTimeField("Data", help_text="Data em que a transação foi criada.")
    last_event_date = models.DateTimeField(
        "Última alteração", help_text="Data da última alteração na transação."
    )
    content = models.TextField("Transação", help_text="Transação no formato json.")

    def __str__(self):
        return self.code

    class Meta:
        ordering = ["-date"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"


class TransactionHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="Transação")
    status = models.CharField(
        "Status", max_length=20, choices=TRANSACTION_STATUS_CHOICES, help_text="Status da transação.",
    )
    date = models.DateTimeField("Data")

    def __str__(self):
        return "{0} - {1} - {2}".format(self.transaction, self.status, self.date)

    class Meta:
        ordering = ["date"]
        verbose_name = "Histórico da transação"
        verbose_name_plural = "Históricos de transações"


# Signals
if PAGSEGURO_LOG_IN_MODEL:
    checkout_realizado.connect(save_checkout)
    notificacao_recebida.connect(update_transaction)

    # API MODELO DE APLICAÇÕES
    pedido_autorizacao_realizado.connect(save_request_authorization)
    notificacao_autorizacao_recebida.connect(save_authorization)
