# -*- coding: utf-8 -*-

import responses
from django.test import TestCase
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils import timezone
from dateutil.parser import parse
from mock import patch

from pagseguro.settings import (
    PRE_APPROVAL_NOTIFICATION_URL, PRE_APPROVAL_REQUEST_URL
)
from pagseguro.api import PagSeguroApiPreApproval

# PreApproval, PreApprovalHistory


notification_response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<preApproval>
    <name>Seguro de Notebook</name>
    <code>FB8389D1F6F6A258849E9F8000C2E173</code>
    <date>2017-10-04T21:09:52-03:00</date>
    <tracker>139095</tracker>
    <status>MY-STATUS</status>
    <reference>meu-id</reference>
    <lastEventDate>2017-10-04T21:10:14-03:00</lastEventDate>
    <charge>AUTO</charge>
    <sender>
        <name>Comprador de Testes</name>
        <email>testes@sandbox.pagseguro.com.br</email>
        <phone>
            <areaCode>11</areaCode>
            <number>99999999</number>
        </phone>
        <address>
            <street>Rua teste</street>
            <number>400</number>
            <complement />
            <district>Bairro</district>
            <city>Cidade</city>
            <state>Estado</state>
            <country>BRA</country>
            <postalCode>CEP</postalCode>
        </address>
    </sender>
</preApproval>'''

# FIXME
"""
pre_approval_request = '''<?xml version="1.0" encoding="UTF-8"?>
<preApprovalRequest>
    <redirectURL>http://www.seusite.com.br/retorno.php</redirectURL>
    <reviewURL>http://www.seusite.com.br/revisao.php</reviewURL>
    <reference>REF1234</reference>
    <sender>
        <name>Nome do Cliente</name>
        <email>cliente@uol.com.br</email>
        <phone>
            <areaCode>11</areaCode>
            <number>56273440</number>
        </phone>
        <address>
            <street>Avenida Brigadeiro Faria Lima</street>
            <number>1384</number>
            <complement>1 Andar</complement>
            <district>Jardim Paulistano</district>
            <postalCode>01452002</postalCode>
            <city>São Paulo</city>
            <state>SP</state>
            <country>BRA</country>
        </address>
    </sender>
    <preApproval>
        <charge>auto</charge>
        <name>Seguro contra roubo do Notebook</name>
        <details>Todo dia 28 será cobrado o valor de R$100,00 referente ao seguro contra roubo de Notebook</details>
        <amountPerPayment>100.00</amountPerPayment>
        <period>Monthly</period>
        <finalDate>2014-01-21T00:00:000-03:00</finalDate>
        <maxTotalAmount>2400.00</maxTotalAmount>
    </preApproval>
</preApprovalRequest>'''
"""

pre_approval_request_response = '''<?xml version="1.0" encoding="UTF-8"?>
<preApprovalRequest>
    <code>A403A4EDD9D9957FF46BCFA89B3DB9F1</code>
    <date>2017-10-11T18:40:23-03:00</date>
</preApprovalRequest>'''


pre_approval_request_error_response = '''<?xml version="1.0" encoding="UTF-8"?>
<errors>
    <error>
        <code>11106</code>
        <message>preApprovalCharge invalid value.</message>
    </error>
</errors>'''


class PagSeguroPreApprovalSignalsTest(TestCase):

    def setUp(self):
        self.url = reverse('pagseguro_receive_notification')
        self.notification_code = 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948'
        self.post_params = {
            'notificationCode': 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948',
            'notificationType': 'preApproval'
        }

    @responses.activate
    def _notification(self, status):
        # mock requests
        responses.add(
            responses.GET,
            '{0}/{1}'.format(
                PRE_APPROVAL_NOTIFICATION_URL, self.notification_code
            ),
            body=notification_response_xml.replace(
                '<status>MY-STATUS</status>', '<status>{0}</status>'.format(status)
            ),
            status=200,
        )

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    def _assert_status(self, signal_mock, status):
        _, kwargs = signal_mock.call_args
        transaction_status = kwargs.get('transaction', {}).get('status')
        self.assertEqual(transaction_status, status)

    @patch('pagseguro.signals.pre_approval_notification.send')
    def test_pre_approval_notification(self, signal_mock):
        self._notification('MY-STATUS')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'MY-STATUS')

    @patch('pagseguro.signals.pre_approval_status_pending.send')
    def test_pre_approval_status_pending(self, signal_mock):
        self._notification('PENDING')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'PENDING')

    @patch('pagseguro.signals.pre_approval_status_active.send')
    def test_pre_approval_status_active(self, signal_mock):
        self._notification('ACTIVE')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'ACTIVE')

    @patch('pagseguro.signals.pre_approval_status_cancelled.send')
    def test_pre_approval_status_cancelled(self, signal_mock):
        self._notification('CANCELLED')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'CANCELLED')

    @patch('pagseguro.signals.pre_approval_status_cancelled_by_receiver.send')
    def test_pre_approval_status_cancelled_by_receiver(self, signal_mock):
        self._notification('CANCELLED_BY_RECEIVER')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'CANCELLED_BY_RECEIVER')

    @patch('pagseguro.signals.pre_approval_status_cancelled_by_sender.send')
    def test_pre_approval_status_cancelled_by_sender(self, signal_mock):
        self._notification('CANCELLED_BY_SENDER')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'CANCELLED_BY_SENDER')

    @patch('pagseguro.signals.pre_approval_status_expired.send')
    def test_pre_approval_status_expired(self, signal_mock):
        self._notification('EXPIRED')
        self.assertTrue(signal_mock.called)
        self._assert_status(signal_mock, 'EXPIRED')

    def test_pre_approval_invalid_status(self):
        with patch('pagseguro.signals.pre_approval_status_pending.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_status_active.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_status_cancelled.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_status_cancelled_by_receiver.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_status_cancelled_by_sender.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_status_expired.send') as signal_mock:
            self._notification('METAL')
            self.assertFalse(signal_mock.called)
        with patch('pagseguro.signals.pre_approval_notification.send') as signal_mock:
            self._notification('METAL')
            self.assertTrue(signal_mock.called)
            self._assert_status(signal_mock, 'METAL')

    @responses.activate
    @patch('pagseguro.signals.pre_approval_create_plan.send')
    def test_pre_approval_create_plan(self, pre_approval_create_plan_mock):
        # mock requests
        responses.add(
            responses.POST,
            PRE_APPROVAL_REQUEST_URL,
            body=pre_approval_request_response,
            status=200,
        )

        pagseguro_api = PagSeguroApiPreApproval(reference='id-unico')
        final_date = timezone.now() + timezone.timedelta(days=180)
        pre_approval_plan_data = {
            'name': 'Seguro contra roubo de Notebook',
            'amount_per_payment': 100,
            'period': 'Monthly',
            'final_date': final_date,
            'max_total_amount': 300,
            'charge': 'auto',
            'details': 'Todo dia 28 será cobrado o valor de R100,00',
        }
        pagseguro_api.create_plan(**pre_approval_plan_data)

        _, kwargs = pre_approval_create_plan_mock.call_args

        code = 'A403A4EDD9D9957FF46BCFA89B3DB9F1'
        data = kwargs.get('data', {})

        self.assertTrue(data['success'])
        self.assertEqual(data['code'], code)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['date'], parse('2017-10-11T18:40:23-03:00'))
        self.assertEqual(
            data['redirect_url'],
            'https://sandbox.pagseguro.uol.com.br/v2/pre-approvals/request.html?code={0}'.format(code)
        )

    @responses.activate
    @patch('pagseguro.signals.pre_approval_create_plan_error.send')
    def test_pre_approval_create_plan_error(self, pre_approval_create_plan_error_mock):
        # mock requests
        responses.add(
            responses.POST,
            PRE_APPROVAL_REQUEST_URL,
            body=pre_approval_request_error_response,
            status=400,
        )

        pagseguro_api = PagSeguroApiPreApproval(reference='id-unico')
        final_date = timezone.now() + timezone.timedelta(days=180)
        pre_approval_plan_data = {
            'name': 'Seguro contra roubo de Notebook',
            'amount_per_payment': 100,
            'period': 'Monthly',
            'final_date': final_date,
            'max_total_amount': 300,
            'charge': 'metal',
            'details': 'Todo dia 28 será cobrado o valor de R100,00',
        }
        pagseguro_api.create_plan(**pre_approval_plan_data)

        _, kwargs = pre_approval_create_plan_error_mock.call_args
        data = kwargs.get('data', {})

        self.assertFalse(data['success'])
        self.assertEqual(data['status_code'], 400)
        self.assertIsNone(data.get('redirect_url'))
        self.assertIsNone(data.get('pre_approval'))
