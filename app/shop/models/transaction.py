from xml.etree import ElementTree
import datetime

from django.db import models
from django.utils.html import format_html

from .product import Product, ProductSize
from .user import User
from ..utils.values import brl

class Transaction(models.Model):
    date = models.DateTimeField('Data')
    code = models.CharField('Código', max_length = 100)
    reference = models.CharField('Referência', max_length=100)
    transaction_type = models.IntegerField('Tipo')
    transaction_status = models.IntegerField('Status')
    last_event_date = models.DateTimeField('Data do Último Evento')
    payment_method_type = models.IntegerField('Tipo do Método de Pagamento')
    payment_method_code = models.IntegerField('Código do Método de Pagamento')
    gross_amount = models.DecimalField('Valor Bruto', decimal_places=2, max_digits=10)
    discount_amount = models.DecimalField('Desconto', decimal_places=2, max_digits=10)
    fee_amount = models.DecimalField('Taxa', decimal_places=2, max_digits=10)
    net_amount = models.DecimalField('Valor Líquido', decimal_places=2, max_digits=10)
    extra_amount = models.DecimalField('Valor Extra', decimal_places=2, max_digits=10)
    installment_count = models.IntegerField('Parcelas')
    sender_name = models.CharField('Nome do Comprador', max_length = 100)
    sender_email = models.CharField('Email do Comprador', max_length = 100)
    sender_phone_code = models.CharField('DDD Telefone Comprador', max_length = 2)
    sender_phone_number = models.CharField('Telefone Comprador', max_length = 9)
    sender_cpf = models.CharField('CPF Comprador', max_length = 11, blank = True, null = True)
    sender = models.ForeignKey(User, verbose_name = 'Comprador', on_delete = models.DO_NOTHING, blank = True, null = True)

    def __str__(self):
        return 'Compra ' + self.reference

    def transaction_items(self):
        items = self.transactionitem_set.all()
        html = '<ul>'
        for item in items:
            if item.product:
                html += '<li>' + str(item.product.id) + ' - ' + item.product.name + ' - TAM ' + str(item.size) + ' - ' + str(item.quantity) + ' x ' + brl(item.amount) + '</li>'
            else:
                html += '<li>Item deletado do estoque - TAM ' + str(item.size) + ' - ' + str(item.quantity) + ' x ' + brl(item.amount) + '</li>'
        html += '</ul>'
        return format_html(html)
    transaction_items.short_description = 'Itens'

    def get_formated_sender_phone_number(self):
        phone = str(self.sender_phone_number).strip()
        if len(phone) == 9:
            return phone[0] + ' ' + phone[1:5] + '-' + phone[5:]
        if len(phone) == 8:
            return phone[0:4] + '-' + phone[4:]
        return phone

    def sender_complete_phone(self):
        return '(' + self.sender_phone_code + ') ' + self.get_formated_sender_phone_number()
    sender_complete_phone.short_description = 'Telefone do Comprador'

    def status(self):
        if self.transaction_status == 1:
            return 'Aguardando Pagamento'
        elif self.transaction_status == 2:
            return 'Em análise'
        elif self.transaction_status == 3:
            return 'Paga'
        elif self.transaction_status == 4:
            return 'Disponível'
        elif self.transaction_status == 5:
            return 'Em disputa'
        elif self.transaction_status == 6:
            return 'Devolvida'
        elif self.transaction_status == 7:
            return 'Cancelada'
        elif self.transaction_status == 8:
            return 'Debitado'
        elif self.transaction_status == 9:
            return 'Retenção Temporária'
        return 'Desconhecido'
    status.short_description = 'Status'

    def parse_values_from_xml(self, xml, cart):
        tree = ElementTree.fromstring(xml)
        self.date = datetime.datetime.fromisoformat(tree.find('date').text)
        self.code = tree.find('code').text
        self.reference = tree.find('reference').text
        self.transaction_type = int(tree.find('type').text)
        self.transaction_status = int(tree.find('status').text)
        self.last_event_date = datetime.datetime.fromisoformat(tree.find('lastEventDate').text)
        self.payment_method_type = int(tree.find('paymentMethod/type').text)
        self.payment_method_code = int(tree.find('paymentMethod/code').text)
        self.gross_amount = float(tree.find('grossAmount').text)
        self.discount_amount = float(tree.find('discountAmount').text)
        self.fee_amount = float(tree.find('feeAmount').text)
        self.net_amount = float(tree.find('netAmount').text)
        self.extra_amount = float(tree.find('extraAmount').text)
        self.installment_count = int(tree.find('installmentCount').text)
        self.sender_name = tree.find('sender/name').text
        email = tree.find('sender/email').text
        self.sender_email = email
        self.sender_phone_code = tree.find('sender/phone/areaCode').text
        self.sender_phone_number = tree.find('sender/phone/number').text
        documents = tree.findall('sender/documents/document')
        not_cpf = True
        for doc in documents:
            if (doc.find('type').text == 'CPF'):
                cpf = doc.find('value').text
                self.sender_cpf = cpf
                self.sender = User.objects.filter(cpf = cpf).first()
                not_cpf = False
        if not_cpf:
            self.sender = User.objects.filter(email = email).first()
        self.save()
        #if parse_items:
        #items = tree.findall('items/item')
        cart_items = cart.get_cart_items()
        for item in cart_items:
            #item_id = int(item.find('id').text)
            #quantity = int(item.find('quantity').text)
            #amount = float(item.find('amount').text)
            trans_item = TransactionItem()
            trans_item.transaction = self
            trans_item.product = item.product
            trans_item.quantity = item.quantity
            trans_item.amount = item.product.real_price()
            trans_item.size = item.size
            trans_item.save()
        cart_items.delete()
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name = 'Transação', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, verbose_name = 'Produto', on_delete = models.DO_NOTHING, blank = True, null = True)
    size = models.ForeignKey(ProductSize, verbose_name = 'Tamanho', on_delete = models.DO_NOTHING, blank = True, null = True)
    quantity = models.IntegerField('Quantidade')
    amount = models.DecimalField('Valor', decimal_places=2, max_digits=10)
