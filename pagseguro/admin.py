from django.contrib import admin

from pagseguro.models import Checkout, Transaction, TransactionHistory, RequestAuthorization, Authorization


class AuthorizationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reference",
        "code",
        "date",
    )
    list_display_links = ("id",)
    search_fields = [
        "code",
    ]
    list_filter = ("date",)


class RequestAuthorizationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reference",
        "code",
        "date",
        "success",
    )
    list_display_links = ("id",)
    search_fields = [
        "code",
    ]
    list_filter = ("date", "success")


class CheckoutAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "date",
        "success",
    )
    list_display_links = ("id",)
    search_fields = [
        "code",
    ]
    list_filter = ("date", "success")


class TransactionHistoryInline(admin.TabularInline):

    list_display = ("id", "transaction", "status", "date")
    list_display_links = ("id",)
    search_fields = [
        "transaction__code",
    ]
    list_filter = ("status", "date")
    model = TransactionHistory
    extra = 0


class TransactionAdmin(admin.ModelAdmin):

    list_display = ("code", "reference", "status", "date", "last_event_date")
    list_display_links = ("code",)
    search_fields = ["code", "reference"]
    list_filter = ("status", "date", "last_event_date")
    inlines = [
        TransactionHistoryInline,
    ]


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RequestAuthorization, RequestAuthorizationAdmin)
admin.site.register(Authorization, AuthorizationAdmin)
