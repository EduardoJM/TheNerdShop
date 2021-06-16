from django.contrib.admin import SimpleListFilter

class PaymentStatusFilter(SimpleListFilter):
    title = 'Status de Pagamento'
    parameter_name = 'transaction_status'

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            (1, 'Aguardando Pagamento'),
            (2, 'Em análise'),
            (3, 'Paga'),
            (4, 'Disponível'),
            (5, 'Em disputa'),
            (6, 'Devolvida'),
            (7, 'Cancelada'),
            (8, 'Debitado'),
            (9, 'Retenção Temporária'),
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(transaction_status = self.value())