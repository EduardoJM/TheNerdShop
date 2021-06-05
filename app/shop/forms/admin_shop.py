from django import forms
from .. import widgets as localWidgets

class ProductImageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': localWidgets.MaterializeFileInput('Foto'),
        }
        fields = '__all__'

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        widgets = {
            'description': localWidgets.MarkdownTextArea()
        }
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        widgets = {
            'top_menu': localWidgets.MaterializeCheckBox('Exibir no Menu Superior?'),
            'parent': localWidgets.MaterializeSelect('Categoria Superior'),
            'icon': localWidgets.MaterializeFileInput('Icone'),
        }
        fields = '__all__'
