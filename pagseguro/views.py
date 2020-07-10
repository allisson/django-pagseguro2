from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from pagseguro.api import PagSeguroApi, PagSeguroAuthorizationApp


@csrf_exempt
@require_http_methods(["POST"])
def receive_notification(request):
    notification_code = request.POST.get("notificationCode", None)
    notification_type = request.POST.get("notificationType", None)

    if notification_code and notification_type == "transaction":
        pagseguro_api = PagSeguroApi()
        response = pagseguro_api.get_notification(notification_code)

        if response.status_code == 200:
            return HttpResponse("Notificação recebida com sucesso.")

    elif notification_code and notification_type == "applicationAuthorization":
        pagseguro_authorization = PagSeguroAuthorizationApp()
        response = pagseguro_authorization.get_notification(notification_code)

        if response.status_code == 200:
            return HttpResponse("Notificação recebida com sucesso.")

    return HttpResponse("Notificação inválida.", status=400)


# apenas para testar
def pagar(request):
    print(request.GET.keys())
    if request.GET.get("hash"):
        hash_code = request.GET.get("hash")
        print(hash_code)
    return render(request, "pagseguro/index.html")