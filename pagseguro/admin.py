# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from pagseguro.models import (
    Checkout, Transaction, TransactionHistory, PreApprovalPlan,
    PreApproval, PreApprovalHistory
)


class CheckoutAdmin(admin.ModelAdmin):

    list_display = ('id', 'code', 'date', 'success',)
    list_display_links = ('id', )
    search_fields = ['code', ]
    list_filter = ('date', 'success')


class TransactionHistoryInline(admin.TabularInline):

    list_display = ('id', 'transaction', 'status', 'date')
    list_display_links = ('id', )
    search_fields = ['transaction__code', ]
    list_filter = ('status', 'date')
    model = TransactionHistory
    extra = 0


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'code', 'reference', 'status', 'date', 'last_event_date',
        'transaction_type',
    )
    list_display_links = ('code', )
    search_fields = ['code', 'reference']
    list_filter = ('status', 'date', 'last_event_date', 'transaction_type')
    inlines = [
        TransactionHistoryInline,
    ]

class PreApprovalPlanAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'amount_per_payment', 'reference', 'period',
        'redirect_code'
    )
    list_display_links = ('id', 'name')
    search_fields = ['redirect_code', 'name', 'reference']
    list_filter = ('charge', 'period')

class PreApprovalHistoryInline(admin.TabularInline):

    list_display = ('id', 'pre_approval', 'status', 'date')
    list_display_links = ('id', )
    search_fields = ['pre_approval__code', ]
    list_filter = ('status', 'date')
    model = PreApprovalHistory
    extra = 0

class PreApprovalAdmin(admin.ModelAdmin):

    list_display = (
        'code', 'tracker', 'reference', 'status', 'date', 'last_event_date'
    )
    list_display_links = ('code', )
    search_fields = ['code', 'reference']
    list_filter = ('status', 'date', 'last_event_date')
    inlines = [
        PreApprovalHistoryInline,
    ]


class PreApprovalPlanAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'amount_per_payment', 'reference', 'period',
        'redirect_code'
    )
    list_display_links = ('id', 'name')
    search_fields = ['redirect_code', 'name', 'reference']
    list_filter = ('charge', 'period')


class PreApprovalHistoryInline(admin.TabularInline):

    list_display = ('id', 'pre_approval', 'status', 'date')
    list_display_links = ('id', )
    search_fields = ['pre_approval__code', ]
    list_filter = ('status', 'date')
    model = PreApprovalHistory
    extra = 0


class PreApprovalAdmin(admin.ModelAdmin):

    list_display = (
        'code', 'tracker', 'reference', 'status', 'date', 'last_event_date'
    )
    list_display_links = ('code', )
    search_fields = ['code', 'reference']
    list_filter = ('status', 'date', 'last_event_date')
    inlines = [
        PreApprovalHistoryInline,
    ]


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PreApprovalPlan, PreApprovalPlanAdmin)
admin.site.register(PreApproval, PreApprovalAdmin)
