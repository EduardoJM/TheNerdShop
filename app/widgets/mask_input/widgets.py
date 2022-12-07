from django.forms import widgets

class MoneyInput(widgets.TextInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['data-mask-money'] = 'on'
        return context

    def value_from_datadict(self, data, files, name):
        value = str(super().value_from_datadict(data, files, name))
        return value.replace(' ', '')

    class Media:
        js = (
            'widgets/mask/vanilla-masker.min.js',
            'widgets/mask/mask.js',
        )
