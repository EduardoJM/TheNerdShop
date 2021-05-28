from django.db.models import fields
from django.forms import ModelForm, widgets
from ..widgets import MarkdownTextArea

class ProductForm(ModelForm):
    
    class Meta:
        widgets = {
            'description': MarkdownTextArea()
        }
        fields = '__all__'
