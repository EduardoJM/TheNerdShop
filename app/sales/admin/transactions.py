from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html

from shop.forms.action import ActionForm
from shop.filters import custom_titled_filter

from ..filters import PaymentStatusFilter

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
                reverse('shop:transaction_update_status', args=[obj.code]),
                reverse('admin:shop_transactionitem_changelist'),
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
        # TODO: create a print registry function here
        pass
