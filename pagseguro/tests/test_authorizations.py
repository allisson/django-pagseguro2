from django.test import TestCase
from django.test import Client

from pagseguro.api import PagSeguroAuthorizationApp


class PagSeguroAuthorizationAppTest(TestCase):
    """
    Para usar os esses testes você precisa:

        - configurar no settings.py as variáveis
            PAGSEGURO_SANDBOX = True
            PAGSEGURO_APP_ID = 'sua appId'
            PAGSEGURO_APP_KEY = 'sua appKey'

        - descomentar as linhas dos meodos abaixo

        - alterar http://127.0.0.1:8000/pagseguro/ pela URL de notificação que você configurou no PagSeguro ou no urls.py

        - no método test_receive_notification substituir o valor do notificationCode por um valor que exista
        no seu SANDBOX do PagSeguro

    """
    def setUp(self) -> None:
        pagseguro = PagSeguroAuthorizationApp(
            permissions=("CREATE_CHECKOUTS", "RECEIVE_TRANSACTION_NOTIFICATIONS"),
            redirectURL="http://seusite.com.br/redirect",
        )
        self.response = pagseguro.get_authorizations()
        self.client = Client()

    # def test_get_authorizations(self):
    #     self.assertEqual(True, self.response.get("success"), self.response)
    #
    # def test_receive_notification_without_data(self):
    #     """Deve retornar status code 400"""
    #     response = self.client.post("http://127.0.0.1:8000/pagseguro/")
    #     self.assertEqual(400, response.status_code)
    #
    # def test_receive_notification(self):
    #     """Deve retornar status code 200"""
    #     data = {"notificationCode": "3DF84F17631563156C5884D01F9C47694513",
    #             "notificationType": "applicationAuthorization"}
    #     response = self.client.post("http://127.0.0.1:8000/pagseguro/", data=data)
    #     self.assertEqual(200, response.status_code)
