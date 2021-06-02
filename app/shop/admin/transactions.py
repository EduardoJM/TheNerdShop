from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html

class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'code',
        'status',
        'reference',
        'transaction_items',
        #'last_event_date',
        'gross_amount',
        'discount_amount',
        'fee_amount',
        'net_amount',
        'extra_amount',
        #'installment_count',
        #'sender_name',
        #'sender_email',
        #'sender_complete_phone',
        #'sender_cpf',
        'user_actions',
    ]

    def user_actions(self, obj):
        return format_html("""
            <a href="%s">Atualizar Status</a>
            """ % (
                reverse('shop:transaction_update_status', args=[obj.code])
            ))
    user_actions.short_description = 'Ações'

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

    def has_add_permission(self, request):
        return False