from django import forms
from image_uploader_widget import widgets as uploader_widgets
from .. import widgets as localWidgets
from widgets.mask_input import MoneyInput

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        widgets = {
            'price': MoneyInput(),
            'discount_price': MoneyInput(),
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
            'icon': uploader_widgets.ImageUploaderWidget('Clique para selecionar uma imagem'),
        }
        fields = '__all__'
