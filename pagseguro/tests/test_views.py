import responses
from django.test import TestCase
from django.urls import reverse

from pagseguro.settings import NOTIFICATION_URL

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


class ReceiveNotificationViewTest(TestCase):

    def setUp(self):
        self.url = reverse('pagseguro_receive_notification')
        self.post_params = {
            'notificationCode': 'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948',
            'notificationType': 'transaction'
        }

    def test_render_without_post_arguments(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.url,
            {'notificationCode': '1'}
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.url,
            {'notificationType': 'transaction'}
        )
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_render_invalid_notification(self):
        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(
                'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948'
            ),
            body='Unauthorized',
            status=401,
        )

        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            'Notificação inválida.',
            status_code=400
        )

    @responses.activate
    def test_render(self):
        # mock requests
        responses.add(
            responses.GET,
            NOTIFICATION_URL + '/{0}'.format(
                'A5182C-C9EF48EF48D2-1FF4AF6FAC82-EB2948'
            ),
            body=notification_response_xml,
            status=200,
        )

        response = self.client.post(self.url, self.post_params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Notificação recebida com sucesso.',
            status_code=200
        )
