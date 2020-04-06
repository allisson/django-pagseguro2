import responses
from django.test import TestCase
from django.urls import reverse

from pagseguro.api import PagSeguroApi, PagSeguroItem
from pagseguro.models import Transaction, TransactionHistory
from pagseguro.settings import CHECKOUT_URL, NOTIFICATION_URL

notification_response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<transaction>
  <date>2014-06-05T22:52:49.000-03:00</date>
  <code>04B68A13-C2CF-4821-8611-F2002636270D</code>
  <reference>REF1234</reference>
  <type>1</type>
  <status>1</status>
  <lastEventDate>2014-06-06T01:10:12.000-03:00</lastEventDate>
  <paymentMethod>
    <type>1</type>
    <code>101</code>
  </paymentMethod>
  <grossAmount>38.00</grossAmount>
  <discountAmount>0.00</discountAmount>
  <feeAmount>2.30</feeAmount>
  <netAmount>35.70</netAmount>
  <extraAmount>0.00</extraAmount>
  <escrowEndDate>2014-06-06T01:05:14.000-03:00</escrowEndDate>
  <installmentCount>1</installmentCount>
  <itemCount>2</itemCount>
  <items>
    <item>
      <id>0001</id>
      <description>Meu item1</description>
      <quantity>1</quantity>
      <amount>14.00</amount>
    </item>
    <item>
      <id>0002</id>
      <description>Meu item2</description>
      <quantity>1</quantity>
      <amount>24.00</amount>
    </item>
  </items>
  <sender>
    <name>Comprador Virtual</name>
    <email>c11004631206281776849@sandbox.pagseguro.com.br</email>
    <phone>
      <areaCode>11</areaCode>
      <number>99999999</number>
    </phone>
  </sender>
  <shipping>
    <address>
      <street>RUA JOSE BRANCO RIBEIRO</street>
      <number>840</number>
      <complement />
      <district>Catolé</district>
      <city>CAMPINA GRANDE</city>
      <state>PB</state>
      <country>BRA</country>
      <postalCode>58410175</postalCode>
    </address>
    <type>3</type>
    <cost>0.00</cost>
  </shipping>
</transaction>'''

checkout_response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<checkout>
  <code>67DB59D3BDBD84EAA4396F929DB350A7</code>
  <date>2014-06-07T00:52:04.000-03:00</date>
</checkout>'''


class PagSeguroSignalsTest(TestCase):

    def setUp(self):
        self.url = reverse('pagseguro_receive_notification')
        self.notificationCode = 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948'
        self.post_params = {
            'notificationCode': 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948',
            'notificationType': 'transaction'
        }

    @responses.activate
    def test_checkout_realizado(self):
        from pagseguro.signals import checkout_realizado

        # load signal function
        def load_signal(sender, data, **kwargs):
            self.assertEqual(
                data['success'], True
            )
            self.assertEqual(
                data['code'], '67DB59D3BDBD84EAA4396F929DB350A7'
            )
            self.assertEqual(
                data['status_code'], 200
            )

        # mock requests
        responses.add(
            responses.POST,
            CHECKOUT_URL,
            body=checkout_response_xml,
            status=200,
        )

        # connect to signal
        checkout_realizado.connect(load_signal)

        # create new checkout
        pagseguro_api = PagSeguroApi()
        pagseguro_api.add_item(
            PagSeguroItem(
                id='1',
                description='My item',
                amount='10.00',
                quantity=1
            )
        )

        # load notification
        pagseguro_api.checkout()

    @responses.activate
    def test_checkout_realizado_com_sucesso(self):
        from pagseguro.signals import checkout_realizado_com_sucesso

        # load signal function
        def load_signal(sender, data, **kwargs):
            self.assertEqual(
                data['success'], True
            )
            self.assertEqual(
                data['code'], '67DB59D3BDBD84EAA4396F929DB350A7'
            )
            self.assertEqual(
                data['status_code'], 200
            )

        # mock requests
        responses.add(
            responses.POST,
            CHECKOUT_URL,
            body=checkout_response_xml,
            status=200,
        )

        # connect to signal
        checkout_realizado_com_sucesso.connect(load_signal)

        # create new checkout
        pagseguro_api = PagSeguroApi()
        pagseguro_api.add_item(
            PagSeguroItem(
                id='1',
                description='My item',
                amount='10.00',
                quantity=1
            )
        )

        # load notification
        pagseguro_api.checkout()

    @responses.activate
    def test_checkout_realizado_com_erro(self):
        from pagseguro.signals import checkout_realizado_com_erro

        # load signal function
        def load_signal(sender, data, **kwargs):
            self.assertEqual(
                data['success'], False
            )
            self.assertEqual(
                data['status_code'], 401
            )
            self.assertEqual(
                data['message'], 'Unauthorized'
            )

        # mock requests
        responses.add(
            responses.POST,
            CHECKOUT_URL,
            body='Unauthorized',
            status=401,
        )

        # connect to signal
        checkout_realizado_com_erro.connect(load_signal)

        # create new checkout
        pagseguro_api = PagSeguroApi()
        pagseguro_api.add_item(
            PagSeguroItem(
                id='1',
                description='My item',
                amount='10.00',
                quantity=1
            )
        )

        # load notification
        pagseguro_api.checkout()

    @responses.activate
    def test_notificacao_recebida(self):
        from pagseguro.signals import notificacao_recebida

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '1'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml,
            status=200,
        )

        # connect to signal
        notificacao_recebida.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_aguardando(self):
        from pagseguro.signals import notificacao_status_aguardando

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '1'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml,
            status=200,
        )

        # connect to signal
        notificacao_status_aguardando.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_em_analise(self):
        from pagseguro.signals import notificacao_status_em_analise

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '2'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>2</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_em_analise.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_pago(self):
        from pagseguro.signals import notificacao_status_pago

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '3'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>3</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_pago.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_disponivel(self):
        from pagseguro.signals import notificacao_status_disponivel

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '4'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>4</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_disponivel.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_em_disputa(self):
        from pagseguro.signals import notificacao_status_em_disputa

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '5'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>5</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_em_disputa.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_devolvido(self):
        from pagseguro.signals import notificacao_status_devolvido

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '6'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>6</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_devolvido.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_cancelado(self):
        from pagseguro.signals import notificacao_status_cancelado

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '7'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>7</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_cancelado.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_debitado(self):
        from pagseguro.signals import notificacao_status_debitado

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '8'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>8</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_debitado.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_notificacao_status_retencao_temporaria(self):
        from pagseguro.signals import notificacao_status_retencao_temporaria

        # load signal function
        def load_signal(sender, transaction, **kwargs):
            self.assertEqual(
                transaction['status'], '9'
            )

        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>9</status>'
            ),
            status=200,
        )

        # connect to signal
        notificacao_status_retencao_temporaria.connect(load_signal)

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_update_transaction(self):
        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml,
            status=200,
        )

        # check transaction
        self.assertFalse(
            Transaction.objects.filter(
                code='04B68A13-C2CF-4821-8611-F2002636270D'
            )
        )

        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction
        self.assertTrue(
            Transaction.objects.filter(
                code='04B68A13-C2CF-4821-8611-F2002636270D'
            )
        )
        transaction = Transaction.objects.get(
            code='04B68A13-C2CF-4821-8611-F2002636270D'
        )

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'aguardando')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>2</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'em_analise')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>3</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='pago'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'pago')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>4</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='pago'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='disponivel'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'disponivel')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>5</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='pago'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='disponivel'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_disputa'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'em_disputa')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>6</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='pago'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='disponivel'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_disputa'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='devolvido'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'devolvido')

        # mock requests
        responses.reset()
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(self.notificationCode),
            body=notification_response_xml.replace(
                '<status>1</status>', '<status>7</status>'
            ),
            status=200,
        )
        # load notification
        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)

        # check transaction history
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='aguardando'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_analise'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='pago'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='disponivel'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='em_disputa'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='devolvido'
            )
        )
        self.assertTrue(
            TransactionHistory.objects.filter(
                transaction=transaction,
                status='cancelado'
            )
        )
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, 'cancelado')
