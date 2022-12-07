from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html
from django.shortcuts import render
from django.db.models import Q

from shop.forms.action import ActionForm
from shop.filters import custom_titled_filter

from ..filters import PaymentStatusFilter
from ..models import Transaction

class TransactionItemAdmin(admin.ModelAdmin):
    action_form = ActionForm
    list_display = ['product', 'quantity']
    list_filter = (
        ('transaction__id', custom_titled_filter('ID da Transação')),
    )

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

    def has_add_permission(self, request):
        return False

class TransactionAdmin(admin.ModelAdmin):
    action_form = ActionForm
    list_display = [
        'date',
        'reference',
        'status',
        'gross_amount',
        'net_amount',
        'user_actions',
    ]
    list_filter = (PaymentStatusFilter, )
    actions = ['print_registry']

    def user_actions(self, obj):
        return format_html("""
            <a class="btn-flat" title="Atualizar Status" href="%s"><i class="material-icons">refresh</i></a>
            <a class="btn-flat" title="Ver Itens" href="%s?transaction__id=%s"><i class="material-icons">shopping_cart</i></a>
            <a class="btn-flat" title="Imprimir Registro"><i class="material-icons">print</i></a>
            """ % (
                reverse('sales:transaction_update_status', args=[obj.code]),
                reverse('admin:sales_transactionitem_changelist'),
                obj.id,
            ))
    user_actions.short_description = 'Ações'

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

    def has_add_permission(self, request):
        return False

    @admin.action(description = 'Imprimir Registros Selecionados')
    def print_registry(self, request, queryset):
        total_len = len(queryset)
        payed = queryset.filter(transaction_status = 3)
        payed_len = len(payed)
        payed_value = 0
        for item in payed:
            payed_value += item.total_price()
        not_payed = queryset.filter(
            Q(transaction_status = 1) | Q(transaction_status = 2)
        )
        not_payed_len = len(not_payed)
        total_itens = 0
        total_price = 0
        for item in queryset:
            total_itens += item.total_itens()
            total_price += item.total_price()
        context = {
            'registry': queryset,
            'payed_percent': (payed_len / total_len) * 100 if total_len != 0 else 0,
            'payed_price': payed_value,
            'not_payed_price': total_price - payed_value,
            'total_itens': total_itens,
            'total_price': total_price,
        }
        return render(request, 'actions/print_registry/multiples.html', context)
        