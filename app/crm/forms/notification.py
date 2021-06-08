from django import forms
from image_uploader_widget import widgets as uploader_widgets
from shop import widgets as local_widgets

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
            'icon': uploader_widgets.ImageUploaderWidget('Clique para selecionar um arquivo!'),
            'banner': uploader_widgets.ImageUploaderWidget('Clique para selecionar um arquivo!'),
        }
        fields = '__all__'
