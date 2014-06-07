# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'pagseguro.views',

    url(
        r'^$', 'receive_notification', name='pagseguro_receive_notification'
    ),

)
