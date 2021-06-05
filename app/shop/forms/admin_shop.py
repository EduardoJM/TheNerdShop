from django.db.models import fields
from django.forms import ModelForm, widgets
from .. import widgets as localWidgets

class ProductImageForm(ModelForm):
    class Meta:
        widgets = {
            'image': localWidgets.MaterializeFileInput('Foto'),
        }
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        widgets = {
            'description': localWidgets.MarkdownTextArea()
        }
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        widgets = {
            'top_menu': localWidgets.MaterializeCheckBox('Exibir no Menu Superior?'),
            'parent': localWidgets.MaterializeSelect('Categoria Superior'),
            'icon': localWidgets.MaterializeFileInput('Ícone'),
        }
        fields = '__all__'
