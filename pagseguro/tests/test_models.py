# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from pagseguro.models import (
    Checkout, Transaction, TransactionHistory, PreApprovalPlan, PreApproval,
    PreApprovalHistory
)


class CheckoutTest(TestCase):

    def test_create_model(self):
        checkout = Checkout.objects.create(
            code='007',
            date=timezone.now(),
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
            date=timezone.now(),
            last_event_date=timezone.now()
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
            date=timezone.now(),
            last_event_date=timezone.now()
        )
        tx_history = TransactionHistory.objects.create(
            transaction=transaction,
            date=timezone.now(),
            status='aguardando'
        )
        self.assertEqual(
            smart_unicode(tx_history),
            '{0} - {1} - {2}'.format(
                tx_history.transaction, tx_history.status, tx_history.date
            )
        )


class PreApprovalPlanTest(TestCase):

    def test_create_pre_approval_plan(self):
        pre_approval_plan = PreApprovalPlan.objects.create(
            name='Seguro contra roubo de Notebook',
            amount_per_payment='100.00',
            period='Monthly',
            final_date=timezone.now(),
            max_total_amount=2400.00,
            charge='auto',
            details='Todo dia 28 será cobrado o valor de R$100,00',
        )
        self.assertEqual(
            smart_unicode(pre_approval_plan), pre_approval_plan.name
        )


class PreApprovalTest(TestCase):

    def test_create_pre_approval(self):
        pre_approval = PreApproval.objects.create(
            code='007',
            tracker='abc',
            reference='nothing',
            status='aguardando',
            date=timezone.now(),
            last_event_date=timezone.now()
        )
        self.assertEqual(
            smart_unicode(pre_approval), pre_approval.code
        )


class PreApprovalHistoryTest(TestCase):

    def test_create_pre_approval_history(self):
        pre_approval = PreApproval.objects.create(
            code='007',
            tracker='abc',
            reference='nothing',
            status='aguardando',
            date=timezone.now(),
            last_event_date=timezone.now()
        )
        pre_approval_history = PreApprovalHistory.objects.create(
            pre_approval=pre_approval,
            date=timezone.now(),
            status='aguardando'
        )
        self.assertEqual(
            smart_unicode(pre_approval_history),
            '{0} - {1} - {2}'.format(
                pre_approval_history.pre_approval,
                pre_approval_history.status,
                pre_approval_history.date
            )
        )
