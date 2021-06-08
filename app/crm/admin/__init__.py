from .notification import NotificationAdmin
from ..models import Notification

from shop.admin import admin_site

admin_site.register(Notification, NotificationAdmin)