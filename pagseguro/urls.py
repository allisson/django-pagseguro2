# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from pagseguro.views import receive_notification

urlpatterns = [
    url(r'^$', receive_notification, name='pagseguro_receive_notification'),
]
