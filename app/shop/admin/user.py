from django.contrib.auth import admin
from django.utils.translation import gettext_lazy as _

from ..forms.action import ActionForm
from ..forms.user import UserChangeForm

class UserAdmin(admin.UserAdmin):
    action_form = ActionForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'cpf', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
