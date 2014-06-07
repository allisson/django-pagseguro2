#-*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

import responses

from pagseguro.settings import NOTIFICATION_URL


notification_response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<transaction>
  <date>2014-06-05T22:52:49.000-03:00</date>
  <code>04B68A13-C2CF-4821-8611-F2002636270D</code>
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


class PagSeguroSignalsTest(TestCase):

    def setUp(self):
        self.url = reverse('pagseguro_receive_notification')
        self.notificationCode = 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948'
        self.post_params = {
            'notificationCode': 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948',
            'notificationType': 'transaction'
        }

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
