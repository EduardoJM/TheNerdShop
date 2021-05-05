from django.contrib.auth.models import User as DjangoUser
from django.db import models

class User(DjangoUser):
    avatar = models.ImageField('Avatar', upload_to = 'images/avatars/')
    cpf = models.CharField('CPF', max_length = 11)
    phone_code = models.CharField('DDD', max_length = 2)
    phone_number = models.CharField('Telefone', max_length = 9)
    billing_address_street = models.CharField('Endereço', max_length=100)
    billing_address_number = models.CharField('Número', max_length=100)
    billing_address_complement = models.CharField('Complemento', max_length=100)
    billing_address_district = models.CharField('Bairro', max_length=100)
    billing_address_postal_code = models.CharField('CEP', max_length=100)
    billing_address_city = models.CharField('Cidade', max_length=100)
    billing_address_state = models.CharField('Estado', max_length=100)
    billing_address_country = models.CharField('País', max_length=100)
