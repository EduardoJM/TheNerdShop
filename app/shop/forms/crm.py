from django import forms
from .. import widgets as local_widgets

class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        widgets = {
            'notification_type': local_widgets.MaterializeSelect('Tipo de Notificação'),
            'user': local_widgets.MaterializeSelect('Usuário'),
            'body': local_widgets.MaterializeTextArea(),
            'email_body': local_widgets.MarkdownTextArea(),
        }
        fields = '__all__'