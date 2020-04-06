from django.test import TestCase
from django.utils import timezone

from pagseguro.models import Checkout, Transaction, TransactionHistory


class CheckoutTest(TestCase):

    def test_create_model(self):
        checkout = Checkout.objects.create(
            code='007',
            date=timezone.now(),
            success=True
        )
        self.assertEqual(
            str(checkout), '{0}'.format(checkout.pk)
        )


class TransactionTest(TestCase):

    def test_create_model(self):
        transaction = Transaction.objects.create(
            code='007',
            reference='nothing',
            status='aguardando',
            date=timezone.now(),
            last_event_date=timezone.now()
        )
        self.assertEqual(
            str(transaction), transaction.code
        )


class TransactionHistoryTest(TestCase):

    def test_create_model(self):
        transaction = Transaction.objects.create(
            code='007',
            reference='nothing',
            status='aguardando',
            date=timezone.now(),
            last_event_date=timezone.now()
        )
        tx_history = TransactionHistory.objects.create(
            transaction=transaction,
            date=timezone.now(),
            status='aguardando'
        )
        self.assertEqual(
            str(tx_history),
            '{0} - {1} - {2}'.format(
                tx_history.transaction, tx_history.status, tx_history.date
            )
        )
