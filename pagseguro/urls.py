# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'pagseguro.views',

    url(
        r'^$', 'receive_notification', name='pagseguro_receive_notification'
    ),

)
