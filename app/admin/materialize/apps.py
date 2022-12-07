from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ExtensionsAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin.materialize'
    verbose_name = _('Materialize Admin')
