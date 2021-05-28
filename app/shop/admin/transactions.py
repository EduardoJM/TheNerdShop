from django.contrib import admin

class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'code',
        'reference',
        'last_event_date',
        'gross_amount',
        'discount_amount',
        'fee_amount',
        'net_amount',
        'extra_amount',
        'installment_count',
        'sender_name',
        'sender_email',
        'sender_complete_phone',
        'sender_cpf',
    ]

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False