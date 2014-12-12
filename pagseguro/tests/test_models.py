# -*- coding: utf-8 -*-
from django.test import TestCase
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from datetime import datetime

from pagseguro.models import Checkout, Transaction, TransactionHistory


class CheckoutTest(TestCase):

    def test_create_model(self):
        checkout = Checkout.objects.create(
            code='007',
            date=datetime.now(),
            success=True
        )
        self.assertEqual(
            smart_unicode(checkout), '{0}'.format(checkout.pk)
        )


class TransactionTest(TestCase):

    def test_create_model(self):
        transaction = Transaction.objects.create(
            code='007',
            reference='nothing',
            status='aguardando',
            date=datetime.now(),
            last_event_date=datetime.now()
        )
        self.assertEqual(
            smart_unicode(transaction), transaction.code
        )


class TransactionHistoryTest(TestCase):

    def test_create_model(self):
        transaction = Transaction.objects.create(
            code='007',
            reference='nothing',
            status='aguardando',
            date=datetime.now(),
            last_event_date=datetime.now()
        )
        tx_history = TransactionHistory.objects.create(
            transaction=transaction,
            date=datetime.now(),
            status='aguardando'
        )
        self.assertEqual(
            smart_unicode(tx_history),
            '{0} - {1} - {2}'.format(
                tx_history.transaction, tx_history.status, tx_history.date
            )
        )
