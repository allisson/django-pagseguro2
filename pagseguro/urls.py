from django.urls import path

from pagseguro.views import receive_notification

urlpatterns = [
    path("", receive_notification, name="pagseguro_receive_notification"),
]
