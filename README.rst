django-pagseguro2
=================

Integração da API v2 do PagSeguro com o Django.

.. image:: https://travis-ci.org/allisson/django-pagseguro2.svg?branch=master
    :target: https://travis-ci.org/allisson/django-pagseguro2

.. image:: https://coveralls.io/repos/allisson/django-pagseguro2/badge.png?branch=master
    :target: https://coveralls.io/r/allisson/django-pagseguro2?branch=master

.. image:: https://img.shields.io/pypi/dm/django-pagseguro2.svg
        :target: https://pypi.python.org/pypi/django-pagseguro2
        :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-pagseguro2.svg
        :target: https://pypi.python.org/pypi/django-pagseguro2
        :alt: Latest Version

.. image:: https://img.shields.io/github/license/allisson/django-pagseguro2.svg
        :target: https://pypi.python.org/pypi/django-pagseguro2
        :alt: License

.. image:: https://img.shields.io/pypi/pyversions/django-pagseguro2.svg
        :target: https://pypi.python.org/pypi/django-pagseguro2
        :alt: Supported Python versions


Instalação e Configuração
-------------------------

Para informações sobre instalação e configuração, acesse:

- `Documentação <http://django-pagseguro-2.readthedocs.org/>`_


Contribuindo
------------

Para contribuir com o projeto, siga os seguintes passos:

#. Clone o repositório ::

    git clone https://github.com/allisson/django-pagseguro2

#. Entre no diretório ::

    cd django-pagseguro2

#. Crie um `virtualenv <http://virtualenvwrapper.readthedocs.org/en/latest/install.html>`_ ::

    mkvirtualenv django-pagseguro2

#. Instale as dependências ::

    make setup

#. Crie um super-usuário ::

    python testapp/manage.py createsuperuser

#. Execute o servidor ::

    make run

#. Abra a área administrativa do Django no navegador ::

    http://localhost:8000/admin

#. Para executar os testes ::

    make test
