Tutorial
============

O django-pagseguro2 necessita do Django versão 1.3+,
lembrando que o suporte ao python3 está presente apenas nas versões 1.5+.

============
Instalação
============

Instale o django-pagseguro2::

    pip install django-pagseguro2

=============
Configuração
=============

Adicione o app pagseguro no INSTALLED_APPS::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'pagseguro',
    )

O django-pagseguro2 suporta as migrações do django 1.7, caso você esteja usando o South, adicione a seguinte configuração no seu settings.py::

    SOUTH_MIGRATION_MODULES = {
        'pagseguro': 'pagseguro.south_migrations',
    }

Adicione as configurações no settings.py::

    PAGSEGURO_EMAIL = 'fulano@cicrano.com'
    PAGSEGURO_TOKEN = 'token'
    PAGSEGURO_SANDBOX = True # se o valor for True, as requisições a api serão feitas usando o PagSeguro Sandbox.
    PAGSEGURO_LOG_IN_MODEL = True # se o valor for True, os checkouts e transações vão ser logadas no database.

Adicione a view que recebe as notificações no urls.py::

    urlpatterns = patterns(
        '',
        url(r'^retorno/pagseguro/', include('pagseguro.urls')),
        # a url de retorno será /retorno/pagseguro/
    )

=================================
Trabalhando com a API de checkout
=================================
Recomendo que você abra um shell do Django para realizar os testes::

    python manage.py shell

Para começar, precisamos importar duas classes, PagSeguroItem e PagSeguroApi::

    >>> from pagseguro.api import PagSeguroItem, PagSeguroApi

O PagSeguroItem representa um item que será adicionado a transação::

    >>> item1 = PagSeguroItem(id='0001', description='Meu item 0001', amount='100.00', quantity=1)
    >>> item1
    <PagSeguroItem: Meu item 0001>
    >>> item1.id
    u'0001'
    >>> item1.amount
    Decimal('100.00')
    >>> item1.quantity
    1
    >>> print(item1.shipping_cost)
    None
    >>> print(item1.weight)
    None

Você pode adicionar informações como custo de envio e peso::

    >>> item2 = PagSeguroItem(id='0002', description='Meu item 0002', amount='150.00', quantity=1, shipping_cost='25.00', weight=500)
    >>> item2
    <PagSeguroItem: Meu item 0002>
    >>> item2.id
    u'0002'
    >>> item2.amount
    Decimal('150.00')
    >>> item2.quantity
    1
    >>> item2.shipping_cost
    Decimal('25.00')
    >>> item2.weight
    500

Agora que temos os itens, podemos fazer o checkout para obter o código da transação::

    >>> pagseguro_api = PagSeguroApi(reference='id-unico-de-referencia-do-seu-sistema')
    >>> # voce poderia passar valores iniciais, ex: pagseguro_api = PagSeguroApi(email='meu@email.com', token='outrotoken')
    >>> # voce pode passar qualquer valor inicial que a documentacao do PagSeguro informa, exceto os itens.
    >>> # o email e token são carregados automaticamente pelas variáveis do settings.
    >>> # adicionando itens
    >>> pagseguro_api.add_item(item1)
    >>> pagseguro_api.add_item(item2)
    >>> # verificando os itens
    >>> pagseguro_api.get_items()
    [<PagSeguroItem: Meu item 0001>, <PagSeguroItem: Meu item 0002>]
    >>> # removendo os itens
    >>> pagseguro_api.clear_items()
    >>> pagseguro_api.get_items()
    []
    >>> # fazendo um checkout
    >>> pagseguro_api.add_item(item1)
    >>> pagseguro_api.add_item(item2)
    >>> data = pagseguro_api.checkout()
    >>> data
    {'date': datetime.datetime(2014, 6, 7, 15, 19, 48, tzinfo=tzoffset(None, -10800)), 'status_code': 200, 'code': u'D0C5A7F8E5E53268849D4F89DA3363E0', 'success': True, 'redirect_url': 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=D0C5A7F8E5E53268849D4F89DA3363E0'}
    >>> # agora basta redirecionar o cliente para o data['redirect_url']
    >>> data['redirect_url']
    'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=D0C5A7F8E5E53268849D4F89DA3363E0'

Você pode consultar os dados de uma transação::

    >>> pagseguro_api = PagSeguroApi()
    >>> data = pagseguro_api.get_transaction('437D1B99-A6E8-46F0-8C00-47B818615AA2')
    >>> data['success']
    True
    >>> data['transaction']
    OrderedDict([(u'date', u'2014-06-07T15:25:36.000-03:00'), (u'code', u'437D1B99-A6E8-46F0-8C00-47B818615AA2'), (u'type', u'1'), (u'status', u'3'), (u'lastEventDate', u'2014-06-07T15:55:37.000-03:00'), (u'paymentMethod', OrderedDict([(u'type', u'1'), (u'code', u'101')])), (u'grossAmount', u'275.00'), (u'discountAmount', u'0.00'), (u'feeAmount', u'14.12'), (u'netAmount', u'260.88'), (u'extraAmount', u'0.00'), (u'escrowEndDate', u'2014-06-21T15:55:37.000-03:00'), (u'installmentCount', u'1'), (u'itemCount', u'2'), (u'items', OrderedDict([(u'item', [OrderedDict([(u'id', u'0001'), (u'description', u'Meu item 0001'), (u'quantity', u'1'), (u'amount', u'100.00')]), OrderedDict([(u'id', u'0002'), (u'description', u'Meu item 0002'), (u'quantity', u'1'), (u'amount', u'150.00')])])])), (u'sender', OrderedDict([(u'name', u'Comprador Virtual'), (u'email', u'c11004631206281776849@sandbox.pagseguro.com.br'), (u'phone', OrderedDict([(u'areaCode', u'11'), (u'number', u'99999999')]))])), (u'shipping', OrderedDict([(u'address', OrderedDict([(u'street', u'RUA JOSE BRANCO RIBEIRO'), (u'number', u'840'), (u'complement', None), (u'district', u'Catol\xe9'), (u'city', u'CAMPINA GRANDE'), (u'state', u'PB'), (u'country', u'BRA'), (u'postalCode', u'58410175')])), (u'type', u'3'), (u'cost', u'25.00')]))])
    >>> data['transaction']['code']
    u'437D1B99-A6E8-46F0-8C00-47B818615AA2'

Passando parâmetros extras na inicialização do PagSeguroApi::
   
    >>> from pagseguro.api import PagSeguroApi
    >>> from decimal import Decimal
    >>> extra_amount = Decimal('20.00')
    >>> sender_email = 'user@email.com'
    >>> sender_name = 'Fulano da Silva'
    >>> sender_area_code = 83
    >>> sender_phone = 11111111
    >>> pagseguro_api = PagSeguroApi(reference='id-unico-de-referencia-do-seu-sistema', extraAmount=extra_amount, senderEmail=sender_email, senderName=sender_name, senderAreaCode=sender_area_code, senderPhone=sender_phone)

Você pode passar qualquer parâmetro http, exceto os relativos aos itens. `Referência. <https://pagseguro.uol.com.br/v2/guia-de-integracao/api-de-pagamentos.html>`_ 


===================================
Trabalhando com Signals de checkout
===================================

Podemos usar o recurso de Signals do Django para capturar informações relacionadas aos checkouts.

Isso é bastante útil para dectectar possíveis problemas na implementação.

Temos os seguintes Signals disponíveis para checkouts:

- **checkout_realizado** (Disparado sempre que um novo checkout for feito).
- **checkout_realizado_com_sucesso**
- **checkout_realizado_com_erro**

Para capturar o Signal **checkout_realizado**::

    >>> from pagseguro.signals import checkout_realizado
    >>> def load_signal(sender, data, **kwargs):
    ...     print(data['success'])
    ...
    >>> checkout_realizado.connect(load_signal)

======================================
Trabalhando com Signals de notificação
======================================

Após a transação ser concluída pelo cliente, o PagSeguro vai enviar uma requisição do tipo POST para uma url que você escolheu previamente sempre que alguma mudança ocorrer no status.

Para ambiente de testes, eu recomendo que você utilize o `PagSeguro Sandbox <http://sandbox.pagseguro.uol.com.br/>`_ em conjunto com o serviço `Runscope <http://www.runscope.com>`_ para conseguir visualizar as notificações.

Quando o PagSeguro envia uma nova notificação, Signals são disparados contendo as informações da transação.

Para cada tipo de status, existe um Signal específico, se você quiser ser notificado apenas quando a compra for paga, você deve capturar o Signal **notificacao_status_pago**.

Temos os seguintes Signals disponíveis para notificações:

- **notificacao_recebida** (Disparado sempre que uma notificação for recebida).
- **notificacao_status_aguardando**
- **notificacao_status_em_analise**
- **notificacao_status_pago**
- **notificacao_status_disponivel**
- **notificacao_status_em_disputa**
- **notificacao_status_devolvido**
- **notificacao_status_cancelado**

Para capturar o Signal **notificacao_recebida**::

    >>> from pagseguro.signals import notificacao_recebida
    >>> def load_signal(sender, transaction, **kwargs):
    ...     print(transaction['status'])
    ...
    >>> notificacao_recebida.connect(load_signal)

Exemplo de um objeto **transaction**::

    >>> transaction
    OrderedDict([(u'date', u'2014-06-07T15:25:36.000-03:00'), (u'code', u'437D1B99-A6E8-46F0-8C00-47B818615AA2'), (u'type', u'1'), (u'status', u'3'), (u'lastEventDate', u'2014-06-07T15:55:37.000-03:00'), (u'paymentMethod', OrderedDict([(u'type', u'1'), (u'code', u'101')])), (u'grossAmount', u'275.00'), (u'discountAmount', u'0.00'), (u'feeAmount', u'14.12'), (u'netAmount', u'260.88'), (u'extraAmount', u'0.00'), (u'escrowEndDate', u'2014-06-21T15:55:37.000-03:00'), (u'installmentCount', u'1'), (u'itemCount', u'2'), (u'items', OrderedDict([(u'item', [OrderedDict([(u'id', u'0001'), (u'description', u'Meu item 0001'), (u'quantity', u'1'), (u'amount', u'100.00')]), OrderedDict([(u'id', u'0002'), (u'description', u'Meu item 0002'), (u'quantity', u'1'), (u'amount', u'150.00')])])])), (u'sender', OrderedDict([(u'name', u'Comprador Virtual'), (u'email', u'c11004631206281776849@sandbox.pagseguro.com.br'), (u'phone', OrderedDict([(u'areaCode', u'11'), (u'number', u'99999999')]))])), (u'shipping', OrderedDict([(u'address', OrderedDict([(u'street', u'RUA JOSE BRANCO RIBEIRO'), (u'number', u'840'), (u'complement', None), (u'district', u'Catol\xe9'), (u'city', u'CAMPINA GRANDE'), (u'state', u'PB'), (u'country', u'BRA'), (u'postalCode', u'58410175')])), (u'type', u'3'), (u'cost', u'25.00')]))])
    >>> transaction.keys()
    [u'date', u'code', u'type', u'status', u'lastEventDate', u'paymentMethod', u'grossAmount', u'discountAmount', u'feeAmount', u'netAmount', u'extraAmount', u'escrowEndDate', u'installmentCount', u'itemCount', u'items', u'sender', u'shipping']
    >>> transaction['status']
    u'3'
    >>> transaction['code']
    u'437D1B99-A6E8-46F0-8C00-47B818615AA2'

==========================================
Logando checkouts e transações no database
==========================================

Sempre que você configura o PAGSEGURO_LOG_IN_MODEL = True, todos os checkouts e transações são logados no database.

Basta acessar o /admin/ e verificar.
