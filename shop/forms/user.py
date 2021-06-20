from django.contrib.auth import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from ..widgets import MaterializeCheckBox, MaterializeSelectMultiple

class UserChangeForm(forms.UserChangeForm):
    class Meta:
        fields = [
            #
            'username',
            # personal info
            'first_name',
            'last_name',
            'email',
            'cpf',
            'avatar',
            # permissions
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            # important dates
            'last_login',
            'date_joined',
        ]
        widgets = {
            'avatar': ImageUploaderWidget('Clique aqui para selecionar um arquivo'),
            'is_active': MaterializeCheckBox('Ativo'),
            'is_staff': MaterializeCheckBox('Membro da Equipe'),
            'is_superuser': MaterializeCheckBox('Status de superusuário'),
            'user_permissions': MaterializeSelectMultiple('Permissões do usuário'),
            'groups': MaterializeSelectMultiple('Grupos'),
        }
