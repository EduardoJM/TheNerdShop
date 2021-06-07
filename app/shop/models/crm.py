from django.db import models

from .user import User

NOTIFICATION_TYPE = [
    ('email', 'E-mail'),
    ('intern', 'Interna'),
    # push notifications are not used for now
    # ('push', 'Push'),
]

class Notification(models.Model):
    notification_type = models.CharField('Tipo', max_length = 20, choices = NOTIFICATION_TYPE)
    title = models.CharField('Título', max_length = 200)
    url = models.CharField('Notification Link', max_length = 255)
    body = models.TextField('Texto da Notificação', max_length = 500, blank = True, null = True)
    email_body = models.TextField('Corpo do E-mail', blank = True, null = True)
    user = models.ForeignKey(User, verbose_name = 'Usuário', on_delete = models.CASCADE)
    created_at = models.DateTimeField('Criado em', auto_created = True)

    def __str__(self):
        return self.title

    @staticmethod
    def send_intern_to_user(user, title, url, body):
        notify = Notification()
        notify.user = user
        notify.url = url
        notify.title = title
        notify.body = body
        notify.notification_type = Notification[1][0]
        notify.save()

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
