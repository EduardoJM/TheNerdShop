from django.contrib.admin import ModelAdmin

from ..forms import NotificationForm

class NotificationAdmin(ModelAdmin):
    form = NotificationForm
    fields = [
        'notification_type', 'url', 'title', 'body', 'email_body', 'user', 'icon', 'banner'
    ]

