from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MaskInputWidgetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'widgets.mask_input'
    verbose_name = _('Money Widget')
