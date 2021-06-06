from django import forms
from django.contrib.admin import helpers
from django.utils.translation import gettext_lazy as _

from ..widgets import MaterializeSelect

class ActionForm(helpers.ActionForm):
    action = forms.ChoiceField(
        label = _('Action:'),
        widget = MaterializeSelect(''),
    )
    