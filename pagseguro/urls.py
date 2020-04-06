from django.conf.urls import url

from pagseguro.views import receive_notification

urlpatterns = [
    url(r"^$", receive_notification, name="pagseguro_receive_notification"),
]
